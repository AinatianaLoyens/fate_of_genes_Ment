### Compute a set of groups based on MCScanX output
library(igraph)
# If error 
# install.packages("igraph")


#### Minimum size of MCScanX group to be accounted for
#### Smaller groups will not be considered

min_size=100

#### Put here the directory where you are 
setwd("C:/Users/ainat/Stage_GAME/To_get_triplet_regions")

#### Put here the name of the collinearity file from MCScanX
data<-readLines("MENTE1834.20230906.recipeA.collinearity",n=-1)

data

### Reads the file and simultaneously generate
### a contig output file (as v1)
### a gene output file 
### From now on you should not modify anything
vector_edges<-character()
genes_edges<-character()
gather_genes<-FALSE
current_align<-character()
genes_edges_names<-character()


for (i in 1:length(data)){
  ### Part analyzing lines from groups of interest (> min_size)
  if(gather_genes==TRUE & (! grepl("Alignment",data[i]))){
    F=strsplit(data[i],":",perl=T)
    G=strsplit(F[[1]][2],"\\s+",perl=T)
    # in this version there is no limit on E-value to add gene couples to the list
    genes_edges_names<- c(genes_edges_names, current_align)
    genes_edges <- c(genes_edges, list(c(G[[1]][2],G[[1]][3])))
  }
  
  ### Part analyzing the ##Alignment lines
  if(grepl("##",data[i]) & grepl("Alignment",data[i])){
    F=strsplit(data[i],"[[:space:]]",perl=T)
    current_align<-paste(F[[1]][2],F[[1]][3],F[[1]][7],sep="#")
    size=as.numeric(sub(".*=","",F[[1]][6]))
    #print(size)
    if(size>=min_size){
       vector_edges<-c(vector_edges,strsplit(F[[1]][7],"&"))
       gather_genes=TRUE
    }else{
       gather_genes=FALSE
    }
    
  }
} 

genes_edges_names

mygraph_genes<-graph(unlist(genes_edges),directed=FALSE)

mygraph_genes<-set_edge_attr(mygraph_genes,"name", value=genes_edges_names)
mygraph_genes
edge_attr(mygraph_genes,"name")[get.edge.ids(mygraph_genes, mygenes[[1]])]
mygenes[[1]]


mygenes<-max_cliques(mygraph_genes,min=2,max=max(degree(mygraph_genes))+1)
get.edge.ids(mygraph_genes, mygenes[[1]])
edge_attr(mygraph_genes,"align")[7090]
head(dec_index_genes)
mygenes[[9593]]
get.edge.ids(mygraph_genes, mygenes[[9593]][c(1,3)])
class(mygenes)
mode(mygenes)
edge_attr(mygenes,"align")


### for contigs
mygraph<-graph(unlist(vector_edges),directed=FALSE)
mygroups<-max_cliques(mygraph,min=2,max=max(degree(mygraph))+1)
dec_index<-rev(order(sapply(mygroups,length)))
outfile_contig=paste("groups_",min_size,"_ment.txt",sep="")
sink(file=outfile_contig)
for(i in dec_index){
  cat(mygroups[[i]]$name,"\n")
}
sink()

### for genes
mygraph_genes<-graph(unlist(genes_edges),directed=FALSE)
mygraph_genes<-set_edge_attr(mygraph_genes,"align", value=genes_edges_names)
mygenes<-max_cliques(mygraph_genes,min=2,max=max(degree(mygraph_genes))+1)
dec_index_genes<-rev(order(sapply(mygenes,length)))
outfile_gene=paste("genes_",min_size,"_ment.txt",sep="")
sink(file=outfile_gene)
for(i in dec_index_genes){
  toprint<-character()
  clique_size=length(mygenes[[i]])
  for(j in 1:(clique_size-1)){
    for(k in 2:clique_size){
      toprint<-paste(toprint,edge_attr(mygraph_genes,"align")[get.edge.ids(mygraph_genes, mygenes[[i]][c(j,k)])], sep=" ")  
    }
  }
  cat(mygenes[[i]]$name,"\t",toprint,"\n")
}
sink()




