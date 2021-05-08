import warnings

import numpy as np
import scipy.sparse as sp
from sklearn.base import TransformerMixin, ClusterMixin, BaseEstimator
from sklearn.cluster._kmeans import _kmeans_single_lloyd, _tolerance, _kmeans_plusplus
from sklearn.exceptions import ConvergenceWarning
from sklearn.utils import check_random_state
from sklearn.utils._openmp_helpers import _openmp_effective_n_threads
from sklearn.utils.extmath import row_norms
from sklearn.utils.validation import _check_sample_weight, check_array

from utils import MAX_ITERATIONS


class KMeans(TransformerMixin, ClusterMixin, BaseEstimator):
    """
    K-Means clustering.

    Parameters
    ----------
    n_clusters : int, default=4
        The number of clusters to form as well as the number of
        centroids to generate.

    init : {'k-means++', 'random'}, callable or array-like of shape \
            (n_clusters, n_features), default='k-means++'
        Method for initialization:

        'k-means++' : selects initial cluster centers for k-mean
        clustering in a smart way to speed up convergence.

        'random': choose `n_clusters` observations (rows) at random from data
        for the initial centroids.

        If an array is passed, it should be of shape (n_clusters, n_features)
        and gives the initial centers.

        If a callable is passed, it should take arguments X, n_clusters and a
        random state and return an initialization.

    searchCentroidSeeds : int, default=10
        Number of time the k-means algorithm will be run with different
        centroid seeds. The final results will be the best output of
        searchCentroidSeeds consecutive runs in terms of inertia.

    stopConditionUsingFrobenius : float, default=1e-4
        Relative stopConditionUsingFrobeniuserance with regards to Frobenius norm of the difference
        in the cluster centers of two consecutive iterations to declare
        convergence.

    Attributes
    ----------
    cluster_centers_ : ndarray of shape (n_clusters, n_features)
        Coordinates of cluster centers. If the algorithm stops before fully
        converging (see ``stopConditionUsingFrobenius`` and ``max_iter``), these will not be
        consistent with ``labels_``.

    labels_ : ndarray of shape (n_samples,)
        Labels of each point

    inertia_ : float
        Sum of squared distances of samples to their closest cluster center.

    n_iter_ : int
        Number of iterations run.

    """

    def __init__(self, n_clusters=4, *, init='k-means++', searchCentroidSeeds=10,
                 stopConditionUsingFrobenius=1e-4):
        self.n_clusters = n_clusters
        self.init = init
        self.stopConditionUsingFrobenius = stopConditionUsingFrobenius
        self.searchCentroidSeeds = searchCentroidSeeds

        # non-parametrized initializations
        self.max_iter = MAX_ITERATIONS
        self.copy_x = True
        # fields which will be initialized later
        self._n_threads = None
        self._stopConditionUsingFrobenius = None
        self._algorithm = None
        self._searchCentroidSeeds = None
        self.cluster_centers_ = None
        self.labels_ = None
        self.inertia_ = None
        self.n_iter_ = None

    def setParams(self, X):
        self._n_threads = None
        self._n_threads = _openmp_effective_n_threads(self._n_threads)
        self._searchCentroidSeeds = self.searchCentroidSeeds
        # stopConditionUsingFrobenius
        self._stopConditionUsingFrobenius = _tolerance(X, self.stopConditionUsingFrobenius)
        self._algorithm = "full" if self.n_clusters == 1 else "elkan"

        # init
        if not (hasattr(self.init, '__array__') or callable(self.init)
                or (isinstance(self.init, str)
                    and self.init in ["k-means++", "random"])):
            raise ValueError(
                f"init should be either 'k-means++', 'random', a ndarray or a "
                f"callable, got '{self.init}' instead.")

        if hasattr(self.init, '__array__') and self._searchCentroidSeeds != 1:
            warnings.warn(
                f"Explicit initial center position passed: performing only"
                f" one init in {self.__class__.__name__} instead of "
                f"searchCentroidSeeds={self._searchCentroidSeeds}.", RuntimeWarning, stacklevel=2)
            self._searchCentroidSeeds = 1

    def _init_centroids(self, X, x_squared_norms, init, random_state,
                        init_size=None):
        """Compute the initial centroids.

        Parameters
        ----------
        X : {ndarray, sparse matrix} of shape (n_samples, n_features)
            The input samples.

        x_squared_norms : ndarray of shape (n_samples,)
            Squared euclidean norm of each data point. Pass it if you have it
            at hands already to avoid it being recomputed here.

        init : {'k-means++', 'random'}, callable or ndarray of shape \
                (n_clusters, n_features)
            Method for initialization.

        init_size : int, default=None
            Number of samples to randomly sample for speeding up the
            initialization (sometimes at the expense of accuracy).

        Returns
        -------
        centers : ndarray of shape (n_clusters, n_features)
        """
        n_samples = X.shape[0]
        n_clusters = self.n_clusters

        if init_size is not None and init_size < n_samples:
            init_indices = random_state.randint(0, n_samples, init_size)
            X = X[init_indices]
            x_squared_norms = x_squared_norms[init_indices]
            n_samples = X.shape[0]

        if isinstance(init, str) and init == 'k-means++':
            centers, _ = _kmeans_plusplus(X, n_clusters,
                                          random_state=random_state,
                                          x_squared_norms=x_squared_norms)
        elif isinstance(init, str) and init == 'random':
            seeds = random_state.permutation(n_samples)[:n_clusters]
            centers = X[seeds]
        elif hasattr(init, '__array__'):
            centers = init
        elif callable(init):
            centers = init(X, n_clusters, random_state=random_state)
            centers = check_array(
                centers, dtype=X.dtype, copy=False, order='C')

        # noinspection PyUnboundLocalVariable
        if sp.issparse(centers):
            centers = centers.toarray()

        return centers

    def fit(self, X):
        """Compute k-means clustering.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            Training instances to cluster. It must be noted that the data
            will be converted to C ordering, which will cause a memory
            copy if the given data is not C-contiguous.
            If a sparse matrix is passed, a copy will be made if it's not in
            CSR format.

        Returns
        -------
        self
            Fitted estimator.
        """
        X = self._validate_data(X, accept_sparse='csr',
                                dtype=[np.float64, np.float32],
                                order='C', copy=self.copy_x,
                                accept_large_sparse=False)

        self.setParams(X)
        random_state = check_random_state(None)
        sample_weight = _check_sample_weight(None, X, dtype=X.dtype)

        # Validate init array
        init = self.init
        if hasattr(init, '__array__'):
            init = check_array(init, dtype=X.dtype, copy=True, order='C')

        # subtract of mean of x for more accurate distance computations
        if not sp.issparse(X):
            X_mean = X.mean(axis=0)
            # The copy was already done above
            X -= X_mean

            if hasattr(init, '__array__'):
                init -= X_mean

        # precompute squared norms of data points
        x_squared_norms = row_norms(X, squared=True)

        kmeans_single = _kmeans_single_lloyd

        best_inertia = None

        for i in range(self._searchCentroidSeeds):
            # Initialize centers
            centers_init = self._init_centroids(
                X, x_squared_norms=x_squared_norms, init=init,
                random_state=random_state)

            # run a k-means once
            labels, inertia, centers, n_iter_ = kmeans_single(
                X, sample_weight, centers_init,
                max_iter=self.max_iter,
                tol=self._stopConditionUsingFrobenius,
                x_squared_norms=x_squared_norms,
                n_threads=self._n_threads)

            # determine if these results are the best so far
            if best_inertia is None or inertia < best_inertia:
                best_labels = labels
                best_centers = centers
                best_inertia = inertia
                best_n_iter = n_iter_

        if not sp.issparse(X):
            if not self.copy_x:
                # noinspection PyUnboundLocalVariable
                X += X_mean
            # noinspection PyUnboundLocalVariable
            best_centers += X_mean

        # noinspection PyUnboundLocalVariable
        distinct_clusters = len(set(best_labels))
        if distinct_clusters < self.n_clusters:
            warnings.warn(
                "Number of distinct clusters ({}) found smaller than "
                "n_clusters ({}). Possibly due to duplicate points "
                "in X.".format(distinct_clusters, self.n_clusters),
                ConvergenceWarning, stacklevel=2)

        # noinspection PyUnboundLocalVariable
        self.cluster_centers_ = best_centers
        self.labels_ = best_labels
        self.inertia_ = best_inertia
        # noinspection PyUnboundLocalVariable
        self.n_iter_ = best_n_iter
        return self

    def fit_predict(self, X, y=None):
        """Compute cluster centers and predict cluster index for each sample.

        Convenience method; equivalent to calling fit(X) followed by
        predict(X).

        Returns
        -------
        labels : ndarray of shape (n_samples,)
            Index of the cluster each sample belongs to.
        """
        return self.fit(X).labels_
