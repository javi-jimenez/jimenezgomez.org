+++
date = '{{ .Date }}'
draft = true
title = '{{ replace .File.ContentBaseName "-" " " | title }}'
+++

# Convención: incluir `image` para que aparezca miniatura en listados.
# Añade una imagen al crear el post colocándola en la carpeta del post y
# estableciendo `image` con el nombre del fichero (ej: `image = "og-image.svg"`).
