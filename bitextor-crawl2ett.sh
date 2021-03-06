#!__BASH__

OUTPUT=/dev/stdout

exit_program()
{
  echo "USAGE: $1 webdir"
  echo "WHERE"
  echo "   webdir   folder downloaded directories"
  exit 1
}

ARGS=$(getopt "bh" $*)
BOILERCOMMAND="__JAVA__ -jar __PREFIX__/share/java/piped-boilerpipe.jar"

set -- $ARGS
for i
do
  case "$i" in
    -h)
      exit_program $(basename $0)
      ;;
    -b)
      shift
      BOILERCOMMAND="cat -"
      ;;
    --)
      shift
      break
      ;;
  esac
done

case $# in
  0)
    WEBCRAWL="/dev/stdin"
    ;;
  1)
    WEBCRAWL="$1"
    ;;
  *)
    exit_program $(basename $0)
    ;;
esac

# Código aquí

#
# 1. Eliminar ficheros repetidos -> (log)
# 2. Obtener tipo y codificación de ficheros
# 3. Quedarse solo con los que tengan tipo html
# 4. Convertir [no UTF-8 -> UTF-8], si hay error -> (log)
# 5. Corregir errores HTML usando Tidy y eliminar las cabeceras HTML
# 6. Incluir el contenido del fichero en base64
#
# Formato final del documento:
# encoding	mimetype	url	content(base_64)
#
# Genera .ett -> encoded and typed text
#

# Not empty files are searched in WEBDIR and they are printer together with their mime type and their encoding
cat $WEBCRAWL | __PYTHON__ -c 'import sys
import magic
import base64

m=magic.open(magic.MAGIC_NONE)
m.load()
for line in sys.stdin:
  fields=line.strip().split("\t")
  if len(fields)>=2:
    url=fields[1]
    content=fields[0]
    #~Mime and encodign
    m.setflags(16|1024)
    magicoutput=m.buffer(base64.b64decode(content)).split(" ")
    magicoutput[0]=magicoutput[0][:-1]
    magicoutput.append(url)
    try:
      magicoutput.append(base64.b64encode(base64.b64decode(content).decode(magicoutput[1].split("=")[1].replace("unknown-8bit","iso-8859-1")).encode("utf8")))
      print "\t".join(magicoutput)
    except LookupError as e:
      sys.stderr.write("Unknown character encoding in file "+url+": "+str(e)+"\n")
  else:
    sys.stderr.write("Wrong line: "+line.strip()+"\n")' | \
__JAVA__ -jar __PREFIX__/share/java/piped-tika.jar -x | eval "$BOILERCOMMAND" | \
__PYTHON__ -c 'import sys
import hashlib
import base64


seen_md5={}
for i in sys.stdin:
  fields = i.strip().split("\t")
  #e = fields[3]
  try:
    e = base64.b64encode(fields[4])
    #Por último, guardamos los datos en un mismo fichero con el formato: encoding   formato   nombre_fichero   base64
    c = hashlib.md5()
    c.update(e)
    #checking for duplicate content (duplicates are discarded)
    if c.hexdigest() in seen_md5:
      sys.stderr.write("Repeated file:\t"+fields[2]+"\tfirst occurrence\t"+seen_md5[c.hexdigest()]+"\n")
    else:
      seen_md5[c.hexdigest()]=fields[2]
      print("{0}\t{1}\t{2}\t{3}".format(fields[0].strip(),fields[1],fields[2],e))
  except UnicodeDecodeError:
    sys.stderr.write("File "+fields[2]+" produced a character encoding error")
' > $OUTPUT


