#constants.py contain all constants need to the project


#User role type - permisos de usuario
#Donde el rol se representa en un binario de 3 bits donde el 1 es si y 0 es no,
#entonces si leer,comentar y escribir tendra un 7 como rol, que en binario es 111
#y para quitar un permiso es solo restar el numero que representa cada permiso,
#por ejemplo le retiro el permiso de poder comentar, es restar 7-2 y dara 5 que en
#binario es 101, con esta manera se puede aumentar mas permisos por si el sistema
#crece, poniendo un nuevo permiso por ejemplo: edicion que representaria a 8
#como el 4 bit.

ReadRole    = 1
CommentRole = 1<<1
WriteRole   = 1<<2
