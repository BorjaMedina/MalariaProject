#MALARIA PROJECT

/	Species Host    Genome size     Genes   Genomic GC
1	Plasmodium berghei	rodents 17954629	 7235
2	Plasmodium cynomolgi    macaques        26181343	5787
3	Plasmodium falciparum   humans  23270305	5207
4	Plasmodium knowlesi     lemures 23462187	4953
5	Plasmodium vivax        humans  27007701	5682
6	Plasmodium yoelii	rodents 22222369	4889
7	Haemoproteus tartakovskyi	birds   17340554	3746
8	Toxoplasma gondii	humans  128105889	15892


1. Gene prediction with the reference genomes
First of all we have to do a gene prediction using GeneMark for each genome files

    gmes_petap.pl --ES --seq ../Genomes/Plasmodium_knowlesi.genome 

Exactly the same command for all of the genomes

2. Cleaning the Haemoproteous sequences
2.1 Cleaning based on the GC content
We have to clean the sequencing data of Haemoproteus tartakovsky. The objective is to clean it from bird sequecnes.
We can create our own parser or use the one in the server. 
With the one in the server would be:

    python removeScaffold.py Haemoproteus_tartakovskyi.raw.genome 35 HaemoproteusFiltered.genome 3000

We have to choose a GC treshold. In this case we are using %GC= 35.
Also we are filering for scaffolds smaller than 3000 nucleotides.
We use 35 because if you look at the disribution of GC you can differentiate 2 peaks, the first one correspondign to the birds sequences going from 30 to 55 and a second one, smaller, from 15 to 35.
Is true taht we are going to include some bird sequences but we will be able to clean them when doing the gene prediction.


2.2 Gene prediction with the output of the step before

    gmes_petap.pl --ES --min_contig 2000 --cores 10 --seq HaemoproteusFitlered.genome

To create the fasta sequences we are going to use the gffParse in the course canvas
To being able to use we have to modify the gff ouput from GeneMark, to make sure that the names are identical

    cat Haemoproteus.gff | sed "s/ GC=.*\tGeneMark.hmm/\tGeneMark.hmm/" > Ht2.gff

We are going to match the genes with the sequences using gffParse.pl

	gffParse.pl -i ../Genomes/HaemoproteusFitlered.genome -g ../03_GenePredictionHaemo/Ht2.gff -b Ht2 -c -p

After that we are going to run a blastp with the output sequences of the parser to identify if we have gene contamination coming from the birds genome.

    nohup blastp -db SwissProt -query ../04_gffParser/Ht2.faa -out blastOutput

We use nohup to leave it running 

Once we have the BLAST output we are goign to select those sequencesscaffolds with bird origin.
To do that we are going to use the parser in the course (dat.Parser.py)
We need uniprot database and taxonomy database

    python datParser.py blastOutput gfParser.fna taxonomy.dat uniprot_sprot.dat > scaffolds.txt

Once we have the scaffolds we have to erase those from our sequence file
For doing that we have created our own python script

    python cleaningScaffolds.py HaemoproteusFitlered.genome scaffolds.txt onlyMalaria.fasta


After that, using the gtf files (obtained after running geneMark) and using gffParse.pl we are going to get the faa sequences for every Plasmodium specie

	gffParse.pl -i ../Genomes/Plasmodium_berghei.genome -g ../01_GenePrediction/genemark.Pb.gtf -b Pb -c -p 
	gffParse.pl -i ../Genomes/Plasmodium_cynomolgi.genome -g ../01_GenePrediction/genemark.Pc.gtf -b Pc -c -p 
	gffParse.pl -i ../Genomes/Plasmodium_yoelii.genome -g ../01_GenePrediction/genemark.Py.gtf -b Py -c -p 
	gffParse.pl -i ../Genomes/Plasmodium_vivax.genome -g ../01_GenePrediction/genemark.Pv.gtf -b Pv -c -p 
	gffParse.pl -i ../Genomes/Toxoplasma_gondii.genome  ../01_GenePrediction/genemark.Tg.gtf -b Tg -c -p 
	gffParse.pl -i ../Genomes/Plasmodium_knowlesi.genome -g ../01_GenePrediction/fixed_Pk.gtf -b Pk -c -p
	gffParse.pl -i ../Genomes/Plasmodium_falciparum.genome -g ../01_GenePrediction/genemark.Pf.gtf -b Pf -c -p
	gffParse.pl -i ../Genomes/Haemoproteus_tartakovskyi.raw.genome -g ../07_finalGenePrediction/finalHt.gtf -b Ht -c -p 

Before being able to run this last gffParse we have to modify the names exactly the same way as before

	(cat Haemoproteus.gff | sed "s/ GC=.*\tGeneMark.hmm/\tGeneMark.hmm/" > Ht2.gff )

We have to fix the Pk genome:

	cat Plasmodium_knowlesi.genome | grep -v  "^chromosome">Plasmodium_knowlesi_fixed.genome

We have to fix the header names of the faa files:

	cat Pk.faa|cut -f 1 > Pk2.faa
	cat Pc.faa|cut -f 1 > Pc2.faa
        cat Pb.faa|cut -f 1 > Pb2.faa
        cat Pv.faa|cut -f 1 > Pv2.faa
        cat Py.faa|cut -f 1 > Py2.faa
        cat Pf.faa|cut -f 1 > Pf2.faa
        cat Tg.faa|cut -f 1 > Tg2.faa
        cat Ht.faa|cut -f 1 > Ht2.faa

We run proteinortho:

	nohup proteinortho6.pl ../{Ht,Pb,Pc,Pf,Pk,Pv,Py,Tg}2.faa 

We run BUSCO for each faa file:

	busco -i ../09_proteinOrtho/Pk2.faa -o Pk -m prot -l apicomplexa -f
        busco -i ../09_proteinOrtho/Pv2.faa -o Pv -m prot -l apicomplexa -f
        busco -i ../09_proteinOrtho/Py2.faa -o Py -m prot -l apicomplexa -f
        busco -i ../09_proteinOrtho/Pf2.faa -o Pf -m prot -l apicomplexa -f
        busco -i ../09_proteinOrtho/Pc2.faa -o Pc -m prot -l apicomplexa -f
        busco -i ../09_proteinOrtho/Pb2.faa -o Pb -m prot -l apicomplexa -f
        busco -i ../09_proteinOrtho/Tg2.faa -o Tg -m prot -l apicomplexa -f
        busco -i ../09_proteinOrtho/Ht2.faa -o Ht -m prot -l apicomplexa -f

We have to modify the duplicates from the Tg BUSCO and saty only with one seque>

        for file in *.faa; do  bash ../../../../../Genomes/fasta2oneline $file >

We are going o create a file for each Plasmodium with links to the .faa files
We are going to parse the files to mix for each BUSCO gene the sequences of all 8 species:
First we have to create a file with the names of all the BUSCO genes we have:


	python joiningBusco2.py ../10_BUSCO/BUSCOgenes.txt

We have to do the alignments of this sequences:

	for line in 11_singlecopy/*.faa; do clustalo -i $line -o 12_alignments/$(basename "$line") -v; done

After the alignments we construct the trees:

	for line in ../*.faa; do  raxmlHPC -s $line -n $(basename "$line") -o Tg -m PROTGAMMABLOSUM62 -p 12345; done

For runnign phylip you ahve ton create a file with all the trees, i used only the bestTrees files:

	cat RAxML_bestTree.* >allTree.tree

After that we run consense tree. When you run phylyp conense it will ask for the rest of parameters

	phylip consense allTree -  rooted trees - 

