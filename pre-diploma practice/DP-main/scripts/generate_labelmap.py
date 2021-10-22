""" usage: generate_labelmap.py [-h] [-i FILEDIR] [-o OUTPUTDIR]

Partition dataset of images into training and testing sets

optional arguments:
  -h, --help            show this help message and exit
  -i FILEDIR, --fileDir FILEDIR
                        'Path to the folder where the faile with label names.'
  -o OUTPUTDIR, --outputDir OUTPUTDIR
                        'Path to the output folder where should be created label_map.pbtxt. Defaults to the same directory where faile with labels names.'
"""
import os
import argparse

def iterate_dir(source, dest):
    source = source.replace('\\', '/')
    dest = dest.replace('\\', '/')
    
    with open(source,'r') as file:
        output_dict ={}
        classname = file.readline().strip()
        count=1
        while len(classname) > 0 :
            output_dict[classname] = count
            classname = file.readline().strip()
            count+=1
      
    with open(dest,'w+') as outfile:
        outfile.truncate(0)
        for i in output_dict.keys():   
           outfile.write("item {\n"+"  id:"+ str(output_dict[i]) + '\n'+'  name:'+"'" +str(i)+"'" +'\n'+ "}\n")


def main():

    # Initiate argument parser
    parser = argparse.ArgumentParser(description="Create label_map.pbtxt with file",
                                    formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        '-i', '--fileDir',
        help='Path to the folder where the faile with label names.',
        type=str,
        default=None
    )
    parser.add_argument(
        '-o', '--outputDir',
        help='Path to the output folder where should be created label_map.pbtxt'
             'Defaults to the same directory where faile with labels names.',
        type=str,
        default=None
    )
    args = parser.parse_args()

    if args.outputDir is None:
        args.outputDir = ('annotations/label_map.pbtxt')
    
    # Now we are ready to start the iteration
    iterate_dir(args.fileDir, args.outputDir)


if __name__ == '__main__':
    main()
