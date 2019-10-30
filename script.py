import os
import re
import pandas as pd


def main(args):
  try:
    os.makedirs('assemblies')
  except:
    pass
  try:
    os.makedirs('fastqc')
  except:
    pass
  try:
    os.makedirs('jellyfish')
  except:
    pass

  names = []
  with open('assemblies.txt', 'r') as r:
     links=r.readlines()
  for i in range(len(links)):
       name = re.search('\w{3}\d{6}', links[i]).group() + re.search('_R\d{1}', links[i]).group() 
       cmd = f'wget -O assemblies/{name}.fastq.gz {links[i]}'
       os.system(cmd)
       cmd = f'gunzip ./assemblies/{name}.fastq.gz'
       os.system(cmd)
       names+= [name]
       cmd = f'fastqc -o fastqc assemblies/{name}.fastq'
       os.system(cmd)
       cmd = f'jellyfish count -m 31 -o jellyfish/{name}kmer_31 -c 3 -s 10000000 assemblies/{name}.fastq'
       os.system(cmd)
       cmd = f'jellyfish histo -o jellyfish/{name}kmer_31.histo jellyfish/{name}kmer_31'
       os.system(cmd)
  cmd = f'spades.py -o spades_SRR292678 -1 assemblies/SRR292678_R1.fastq -2 assemblies/SRR292678_R2.fastq'
  os.system(cmd)
  cmd = 'spades.py -t 32 -k 31 -o spades_3_libs  -1 assemblies/SRR292678_R1.fastq -2 assemblies/SRR292678_R2.fastq --mp1-1 SRR292862_R1.fastq --mp1-2 SRR292862_R2.fastq --mp2-1 SRR292770_R1.fastq --mp2-2 SRR292770_R2.fastq'
  os.system(cmd)
  
  cmd = 'barrnap -o rRNA.fasta < spades_3_libs/scaffolds.fasta > rRNA.gff'
  os.system(cmd)

  cmd = 'prokka --centre X --compliant spades_3_libs/scaffolds.fasta'
  os.system(cmd)
  
if __name__=='__main__':
    '''parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)    
    parser.add_argument('-spades', type=str, default='~/SPAdes-3.13.1/spades.py',
                        help='Path to spader.py file')
    args = parser.parse_args()'''
    main(args)

