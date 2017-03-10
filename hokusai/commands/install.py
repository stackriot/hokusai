import os
import urllib
import shutil

from distutils.dir_util import mkpath

import boto3

from hokusai.common import print_red, print_green

def install(kubectl_version, platform, install_to, install_kubeconfig_to, bucket_name, key_name, bucket_region):
  try:
    print_green("Downloading and installing kubectl...")
    urllib.urlretrieve("https://storage.googleapis.com/kubernetes-release/release/v%s/bin/%s/amd64/kubectl" % (kubectl_version, platform), os.path.join('/tmp', 'kubectl'))
    os.chmod(os.path.join('/tmp', 'kubectl'), 0755)
    shutil.move(os.path.join('/tmp', 'kubectl'), os.path.join(install_to, 'kubectl'))
  except Exception, e:
    print_red("Error installing kubectl: %s" % repr(e))
    return -1

  try:
    print_green("Configuring kubectl...")
    if not os.path.isdir(install_kubeconfig_to):
      mkpath(install_kubeconfig_to)

    bucket = boto3.resource('s3').Bucket(bucket_name)
    bucket.download_file(key_name, os.path.join(install_kubeconfig_to, 'config'))

  except Exception, e:
    print_red("Error configuring kubectl: %s" % repr(e))
    return -1

  return 0
