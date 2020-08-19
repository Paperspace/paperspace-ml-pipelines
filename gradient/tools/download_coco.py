import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Download COCO dataset")
    parser.add_argument('--inputs', '-i', type=str, default='/coco',
                        help='input directory for coco dataset')
    return parser.parse_args()

def get_coco_dataset(url, filedir):
    from urllib.request import urlopen
    from tempfile import NamedTemporaryFile
    from shutil import unpack_archive
    zipurl = url
    with urlopen(zipurl) as zipresp, NamedTemporaryFile() as tfile:
        tfile.write(zipresp.read())
        tfile.seek(0)
        unpack_archive(tfile.name, filedir, format = 'zip')

def main():
    # Get arguments.
    args = parse_args()
    # Upscale coco.
    get_coco_dataset('http://images.cocodataset.org/annotations/annotations_trainval2017.zip', args.inputs)

main()