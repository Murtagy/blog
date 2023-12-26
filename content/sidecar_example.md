Title: Snippets. Sidecar deployment
Date: 2023-12-26
Tags: kubernetes, sidecar, python

I published a small snippet how to deploy two webservices together in a sidecar. [Here!](https://github.com/Murtagy/sidecar-example)  


The context about sidecar you need to know is located below.  

A *Pod* is a group of one or more [containers](https://kubernetes.io/docs/concepts/containers/).  
What containers in a pod share - network namespace (locahost), [process namespace](https://kubernetes.io/docs/tasks/configure-pod-container/share-process-namespace/), [storage](https://kubernetes.io/docs/tasks/access-application-cluster/communicate-containers-same-pod-shared-volume/).  
What they do not share (directly) - filesystem, resources.  

This effectively means that you can run a service in a sidecar along with the main service and both are web applications. Web apps can talk via localhost to each other. This might be not clearly visible from reading official desription with examples around using system utilities or a single web service.  
When it might be useful - is when 2 webservices use shared code and MUST run using same version of that shared code.  
That's all. Good luck, sailor!  