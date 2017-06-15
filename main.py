import pykube
import os
import json

api = None

class Watcher(object):

    def __init__(self):
        self.api = self.get_api()

    def get_api(self):
        kubeconfig = '/root/.kube/config'
        if os.path.isfile(kubeconfig):
            # locally
            return pykube.HTTPClient(
                pykube.KubeConfig.from_file(kubeconfig))
        else:
            # from a pod
            return pykube.HTTPClient(
                pykube.KubeConfig.from_service_account())

    def watch(self):
        watch = pykube.Node.objects(self.api).watch()
        #filter on added
        # watch is a generator:
        for e in watch:
            if e.type == 'ADDED':
                pool_maps = self.get_pools_map()
                


    def get_pools_map(self):
        nodes = pykube.Node.objects(self.api)
        pools = {}
        for node in nodes:
            metadata = node.obj['metadata']
            capacity = node.obj['status']['capacity']
            pool_name = self.get_pool_name(metadata['name'])

            #'alpha.kubernetes.io/nvidia-gpu' is not present on some nodes instead of reporting 0
            gpu_per_instance = 0
            if 'alpha.kubernetes.io/nvidia-gpu' in capacity:
                gpu_per_instance = capacity['alpha.kubernetes.io/nvidia-gpu']

            if pool_name in pools:
                pools[pool_name]['size'] += 1
            else:
                pools[pool_name] = {'name': pool_name, 'instanceId': metadata['labels']['beta.kubernetes.io/instance-type'], 'size': 1, 'cpuPerInstance': capacity['cpu'], 'gpuPerInstance': gpu_per_instance}

        return pools
            

    def get_pool_name(self, name):
        name_parts = name.split('-')  
        if len(name_parts) != 4:
            raise ValueError('Kubernetes node name was malformed and cannot be processed.')
        return name_parts[1]


def main():
    watcher = Watcher()
    watcher.watch()

if __name__ == '__main__':
    main()
