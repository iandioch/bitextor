#!__BASH__

OUTPUT=/dev/stdout

exit_program()
{
  echo "USAGE: $1 webdir"
  echo "WHERE"
  echo "   webdir   folder downloaded directories"
  exit 1
}

langs=""
FILE="/dev/stdin"

ARGS=$(getopt "hl:" $*)

set -- $ARGS
for i
do
  case "$i" in
    -h|--help)
      exit_program $(basename $0)
      ;;
    -l|--languages)
      shift
      langs="-l $1"
      shift
      ;;
    --)
      shift
      break
      ;;
  esac
done

case $# in
  0);;
  1)
    FILE="$1"
    ;;
  *)
    exit_program $(basename $0)
    ;;
esac


cat $FILE | __JAVA__ -jar __PREFIX__/share/java/piped-tika.jar -t | \
__PYTHON__ -c '
#
# 1. Read lines from .ett file
# 2. For eac line, the HTML is cleaned and the language is detected for the raw text
# 3. Output is printed following the format:
#
# language	encoding	mimetype	url	content(base_64)
#
#

import sys
import base64
from HTMLParser import HTMLParser
import langid
import argparse
import socket
import re

#reload(sys)
#sys.setdefaultencoding("UTF-8")

oparser = argparse.ArgumentParser(description="Script that reads the output of bitextor-webdir2ett and, for each line (lines correspond to files in de website) the language of the document is detected and this information is added to the information about the documents.")
oparser.add_argument("ett_path", metavar="FILE", nargs="?", help="File containing the output of bitextor-webdir2ett (if undefined, the script reads from the standard input)", default=None)
oparser.add_argument("-l", "--languages", help="List accepted languages represented as a comma separated language codes list", dest="langlist", default=None)
options = oparser.parse_args()

langs=[]
if options.langlist != None:
  langs=options.langlist.strip().split(",")

if options.ett_path != None:
  reader = open(options.ett_path,"r")
else:
  reader = sys.stdin

#Reading line by line from the standard output
for line in reader:
  linefields=line.strip().split("\t")
  #decoding the b64 original webpage
  if len(linefields)>=5:
    parsed_text=base64.b64decode(linefields[4]).decode("utf-8")

    if len(parsed_text)>0:
      #detecting language
      lang, conf = langid.classify(parsed_text)
      if len(langs)==0 or lang in langs:
        linefields.insert(0,lang)
        e = base64.b64encode(parsed_text.encode("utf-8"))
        del linefields[-1]
        linefields.append(e)
        print "\t".join(linefields)' $langs 

