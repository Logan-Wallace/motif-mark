# motif-mark
motif-mark-oop.y is an object oriented program that will identify exons and motifs within a gene and write the results to a png image.

It will take as input two files;  
The first will be a text file (see 'Fig_1_motifs.txt' within this repo) containing motifs of interest. Motif mark can handle ambiguos nucleotides written per IUPAC guidelines (https://en.wikipedia.org/wiki/Nucleic_acid_notation).  
The other file will be a fasta file (see 'Figure_1.fasta' within this repo) containing the genes we would like to search for exons and motifs.  
The corresponding png file will be written out as motif-marks.png

## Installation

To download this repository - 

```bash
git clone https://github.com/Logan-Wallace/motif-mark.git
```

## Usage

-f The name of the fasta file containing gene sequences.

-m The name of the text file containing the motifs we are searching the genes for.

```bash
python motif-mark-oop.y -f "genes.fa" -m "motifs.txt"
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.
