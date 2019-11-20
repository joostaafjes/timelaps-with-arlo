find . -maxdepth 1 -type f -name '*.mp3' -print0 |
  sort -z |
  xargs -0 cat -- >> out.mp33
mv out.mp33 out.mp3
