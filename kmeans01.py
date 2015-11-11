import sys
from collections import Counter
import os 
from sets import Set
import numpy as np

vocabulary=Set([])
documents=[]
clusters=[]

def prepare_vocabulary(path):
    global vocabulary
    words=[]
    if os.path.isdir(path)==False: 
        print err('not a directory')
        return
    for (root,dirs,files) in os.walk(path):
        for file in files:
            filepath=os.path.join(path,file)
            for line in open(filepath,'r').readlines():
                words=words+line.split()
    vocabulary.update(words)

def build_vectors(path):
    global vocabulary,documents
    if os.path.isdir(path)==False: 
        print err('not a directory')
        return
    for (root,dirs,files) in os.walk(path):
        for file in files:
            words=[]
            filepath=os.path.join(path,file)
            for line in open(filepath,'r').readlines():
                words=words+line.split()
            documents.append({'path':filepath,'vector':np.array([ 1 if j in words else 0 for j in vocabulary])})

def measure_distance(di,dj):
    global documents
    return np.sum((di-dj)*(di-dj))

def create_clusters(number):
    global documents,clusters
    for i in range(int(number)):
        clusters.append({'id':i,'documents':[documents[i]],'centroid':documents[i]['vector']})


def fill_clusters():
    global clusters,documents
    for d in documents:
        distances=[]
        for c in clusters:

            distance=measure_distance(c['centroid'],d['vector'])
            distances.append({'c_id':c['id'],'d_path':d['path'],'distance':distance})
        min_distance=sorted(distances,key=lambda k:k['distance'])
        #print min_distance
        t = min_distance[0]['c_id']
        #print t,d,c
        if not d in clusters[t]['documents']:
            clusters[t]['documents'].append(d)

def compute_centroid():
    for c in clusters:
        centroid=np.array([])
        for d in c['documents']:
            centroid=np.concatenate((centroid,d['vector']))
        ndocs=len(c['documents'])
        centroid=centroid.reshape(ndocs,len(c['documents'][0]['vector']))
        centroid= np.sum(centroid,axis=0)/ndocs
        c['centroid']=centroid
def err(string):
    return '\x1b[%sm%s\x1b[0m' % (';'.join(['31','1']), string)
    
def run(arg):
    global vocabulary,document,clusters
    try:
        print 'Directory: ',arg[1]
        print 'Value of k: ',arg[2]
        prepare_vocabulary(arg[1])
        build_vectors(arg[1])
        create_clusters(arg[2])
        fill_clusters()
        compute_centroid()
        for i in clusters:print i['centroid']
        fill_clusters()
        compute_centroid()
        for i in clusters:print i['centroid']
        fill_clusters()
        compute_centroid()
        for i in clusters:print i['centroid']        
        fill_clusters()
        compute_centroid()
        
        for i in clusters:print i['centroid']

    except:
        print err('Application Error')
        print '[Message] application invoke. format: app <directoryname> <value of k> '
        
if __name__=='__main__':
    run(sys.argv)
    
