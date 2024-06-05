library(omnibus) # for insertion functions

setwd("C:/Users/ainat/Stage_GAME/caracterise_loss/softcode")

file_list <- list.files("Alignments", full.names = TRUE) #To get the files to order, in the directory Alignments

for (index in 1:length(file_list)) {
  read.table(file_list[index], sep=" ") -> dat
  head(dat)

  sum(grepl("ME",dat$V1))
  #49
  sum(grepl("ME",dat$V2))
  #65
  sum(grepl("ME",dat$V3))
  #51

  # Contig prioritaire: B, puis C puis A
  # De manière automatisée:pwd

  priority<-order(apply(dat,2,function(x){sum(grepl("ME",x))}),decreasing=TRUE)

  # How many genes are there on each line?
  nb_genes<-apply(dat,1,function(x){sum(grepl("ME",x))})
  nb_genes

  # Separation of the dataset in lines with 2+ genes and others
  dat_full<-dat[nb_genes==3,]
  dat_holes<-dat[nb_genes<=2,]

  # Ordering the full dataset based on primary contig order -- order does the job
  dat_full_ordered<-dat_full[order(dat_full[,priority[1]]),]

  # Check
  # presence d'une ligne incohérente  (indice 19) détecté par analyse manuelle
  # a voir si on peut automatiser ou si on doit faire qqch pour ces lignes.
  dat_full_ordered[12:15,]


  # General function to compute an insertion score, accounting for holes ||| between a gene g an a contig vec
  # Score is high (1) when a gene finds its place between two elements of vec
  # Score is low when g is a hole
  # score is 0 when g cannot be placed between two consecutive vec elements 
  # We only account for holes in the line to be inserted, as the data frame should not contain any
  ### version of the insertion score function
  ### which account for quantum holes,
  ### i.e multiple genes at a single position.
  is_insertable_quantum <-function(g,vec){
    if(g=="||||||||||||||||||||"){
      return(rep(0.001,length(vec)-1))
    }else{
      local_score<-numeric(length=length(vec)-1)
      for(i in 1:length(local_score)){
        genes_bef<-strsplit(x=vec[i],split="#")[[1]] # if pos before is a virtual gene  -- aka a hole -- with 2 possibilites
        genes_aft<-strsplit(x=vec[i+1],split="#")[[1]] # if pos after is a virtual gene  -- aka a hole -- with 2 possibilites
        if((min(genes_bef)<=g  & g<=max(genes_aft)) | (min(genes_aft)<=g  & g<=max(genes_bef))){
          local_score[i]<-1
        }else{
          local_score[i]<-0
        }
      }
      return(local_score)
    }
  }


  # The function to insert a line in a dataframe
  # while changing the holes into virtual genes
  # and checking if the insertion should change the adjacent virtual genes

  insert_line_at_pos<-function(data, line,pos){
    if(pos==0){
      # Changing all holes on line to be inserted into the closest value
      # No other changes required in this case
      for(i in 1:3){
        line[,i]<-ifelse(grepl("\\|\\|",line[,i]),data[1,i],line[,i])
      }
      return(insertRow(x=line,into=data,at=1, before=TRUE))
    }
    if(pos==nrow(data)){
      # Changing all holes on line to be inserted into the closest value
      # No other changes required in this case
      for(i in 1:3){
        line[,i]<-ifelse(grepl("\\|\\|",line[,i]),data[pos,i],line[,i])
      }
      return(insertRow(x=line,into=data,at=pos, before=FALSE))
    }  
    # Other cases
    # Virtual genes should be inserted in place of holes
    for(i in 1:3){
      line[,i]<-ifelse(grepl("\\|\\|",line[,i]), # if there is a hole in the line to insert
                      ifelse(grepl("#",data[pos,i]) |  grepl("#",data[pos+1,i]), #is one of the adjacent line is also a hole? 
                              ifelse(grepl("#",data[pos,i]), data[pos,i],  data[pos+1,i]), # yes: we duplicate it
                              paste(as.character(data[pos,i]),as.character(data[pos+1,i]),sep="#")), # no: we create one
                      line[,i]) # if no hole we just keep the value as it is
    }
    # Then, for each adjacent line, if there is a virtual gene pair adjacent to a real gene, 
    # The pair borders should be restricted not to overlap the real position
    for(i in 1:3){
      # check line before
      if(grepl("#",data[pos,i]) & (!grepl("#",line[,i]))){
        #cat("Hole edition  before at ",data[pos,i], " with ",line[,i],"\n")
        borders=strsplit(data[pos,i],"#")[[1]]
        borders[2] = line[,i]
        data[pos,i]<-paste(borders, collapse="#")
      }
      # then line after
      if(grepl("#",data[pos+1,i]) & (!grepl("#",line[,i]))){
        #cat("Hole edition after at ",data[pos+1,i], " with ",line[,i],"\n")
        borders=strsplit(data[pos+1,i],"#")[[1]]
        #cat("Border decomp ", borders," with length ",length(borders),"\n")
        borders[1] = line[,i]
        data[pos+1,i]<-paste(borders,collapse="#")
        #cat("New line after ",data[pos+1,i],"\n" )
      }
    }
    return(insertRow(x=line,into=data,at=pos, before=FALSE))
  }




  # We build the function that takes a data frame, a column number, and a line to insert,
  # check at which positions the insertion can take place,
  # and make the insertion
  ### version of the function that considers holes a being "both" the genes that surround them
  find_position_into_dataframe_quantum <- function(data,line,priority){
    # we suppose data is ordered on the highest priority column only
    score=100*is_insertable_quantum(line[,priority[1]],data[,priority[1]])+10*is_insertable_quantum(line[,priority[2]],data[,priority[2]])+is_insertable_quantum(line[,priority[3]],data[,priority[3]]) 
    if(max(score)<1){
      cat("No good insertion for line ", as.character(line),"\n") # debug
      # We will add the line as first or last in the table
      # Based on the closest gene in decreasing priority order
      for(p in priority){
        if(line[,p]!="||||||||||||||||||||"){
          line_pos=as.numeric(substr(line[,p],14,100))
          tmp_pos <- numeric(2) # two possibilities: start or end
          ### We should account for the fact that a start or end may be quantum -- is this even possible?
          ### Apparently not, as insertions on the border have information only on one side -> nothing special
          tmp_pos[1]<-as.numeric(substr(data[1,p],14,100))
          tmp_pos[2]<-as.numeric(substr(data[nrow(data),p],14,100))
          tmp_pos <- abs(line_pos-tmp_pos)
          # if start and end at same distance
          # we insert at end
          best_insert_pos<- ifelse(tmp_pos[1] < tmp_pos[2],0,nrow(data))
          cat("Insertion done for line ", as.character(line),"at line ",best_insert_pos,"\n")
          return(insert_line_at_pos(data,line,best_insert_pos))
        }
      }
    }else{
      insert_pos=which(score==max(score))
      if(length(insert_pos)>=2){
        cat("Multiple insertions possible for line ", as.character(line),"with ", insert_pos,"\n")
        # If more than one insertion is possible, 
        # we insert at the place where the genes are closer to existing ones
        # based on priority
        for(p in priority){
          if(line[,p]!="||||||||||||||||||||"){
            line_pos=as.numeric(substr(line[,p],14,100))
            tmp_pos <-matrix(0,nrow=2,ncol=length(insert_pos))
            
            ### We have to account for the fact that virtual genes are present on the sides of multiple insertions
            ### In this case the distance computed should be with the first term of the virtual gene if this virtual gene is before
            ### and second term if this virtual gene is after 
            
            for(i in 1:length(insert_pos)){
              before<-strsplit(data[insert_pos[i],p],"#")[[1]]
              #cat("Multiple position close to virtual gene\n")
              #cat("Before:",before,"\n")
              tmp_pos[1,i]<-as.numeric(substr(before[1],14,100))
              
              after<-strsplit(data[insert_pos[i]+1,p],"#")[[1]]
              #cat("After:",after,"\n")
              tmp_pos[2,i]<-as.numeric(substr(after[length(after)],14,100))
            }
            tmp_pos[1,] <- abs(line_pos-tmp_pos[1,])
            tmp_pos[2,] <- abs(line_pos-tmp_pos[2,])
            delta <- apply(tmp_pos,2,min)
            # if multiple positions are at same distance
            # we take the one where the interval is smaller
            if(sum(delta==min(delta)) > 1){
              best_insert<-which(colSums(tmp_pos)==min(colSums(tmp_pos)))[1]
            }else{
              best_insert<-which(delta==min(delta)) 
            }
            best_insert_pos<-insert_pos[best_insert]
            cat("Insertion done for line ", as.character(line),"at line ",best_insert_pos,"\n")
            cat("Between lines ", as.character(data[best_insert_pos,]),"\n")
            cat("And ", as.character(data[best_insert_pos+1,]),"\n")
            return(insert_line_at_pos(data,line,best_insert_pos))
          }
        }
      }else{
        # If we found a place to insert line
        # We insert it, and change any holes on it with the gene value located just before.
        # This way, the virtual insertion table dones not contain ny holes
        cat("Insertion done for line ", as.character(line),"at line ",insert_pos,"\n")
        return(insert_line_at_pos(data,line,insert_pos))
      }
    }
    # If we arrive here it that everything failed -- it should not happen.
    cat("ERROR: No insertion at all for line ", as.character(line),"\n") # debug
    return(data)
  }


  ### Main code

  # We create a virtual table that will hold all lines, fulle and inserted, 
  # with inserted lines having their holes replaced by placeholders
  dat_full_ordered_virtual<-dat_full_ordered

  # We insert each line with hole
  for (i in 1:nrow(dat_holes)){
    cat(i,"\n") #debug
    line<- dat_holes[i,]
    cat(as.character(line),"\n") #debug
    dat_full_ordered_virtual<-find_position_into_dataframe_quantum(dat_full_ordered_virtual,line,priority)
  }

  # Finally we create the real table by using the names from the virtual table
  dat_final<- dat[as.character(rownames(dat_full_ordered_virtual)),]

  dat_final
  ###Creating the output file
  filename<-basename(file_list[index])
  cat("full name current input file", file_list[index], "\n")
  cat("current input file", filename, "\n")
  numbers <- as.numeric(unlist(regmatches(filename, gregexpr("[0-9]+", filename))))
  #numbers <- gsub("[^0-9]", " ", filename)
  #numbers <- as.numeric(unlist(strsplit(numbers, " ")))
  cat("numbers are", numbers, "\n")
  output_filename <- paste0("align", paste(numbers, collapse = "_"), "_ordered.txt")
  #output_filename <- paste0("align", numbers[1], "_", numbers[2], "_", numbers[3], "_ordered.txt")
  cat("Nom du fichier de sortie", output_filename)

  write.table(x = dat_final, file = output_filename, col.names = FALSE, row.names = FALSE, quote = FALSE)
}
#cat("file_list",file_list)
### debug start here


