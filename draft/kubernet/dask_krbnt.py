# Example usage
from dask.distributed import Client
import dask.array as da
from dask_kubernetes import KubeCluster


if __name__ == '__main__':

    cluster = KubeCluster.from_yaml('worker-spec.yml')
    cluster.scale(10)  # specify number of workers explicitly
    cluster.adapt(minimum=1, maximum=100)  # or dynamically scale based on current workload

    # Connect Dask to the cluster
    client = Client(cluster)

    # Create a large array and calculate the mean
    array = da.ones((1000, 1000, 1000))
    print(array.mean().compute())  # Should print 1.0
