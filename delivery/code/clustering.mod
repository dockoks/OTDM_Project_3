#Below we define the AMPL model for clustering

param m;
param k;
param d{1..m, 1..m};
var x{1..m, 1..m} binary;

minimize f: sum{i in 1..m, j in 1..m} d[i,j]*x[i,j];
subject to c1{i in 1..m}: sum{j in 1..m} x[i,j] = 1;
# This constraint ensures every point belongs to 1 cluster
subject to c2: sum{j in 1..m} x[j,j] = k;
# This constraint ensure that there are exactly k clusters
subject to c3{i in 1..m, j in 1..m}: x[j,j] >= x[i,j];
# This constraint ensures that a point can only be part of a cluster that exists
