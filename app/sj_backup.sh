#!/bin/bash

# Verificar si se proporcionó un argumento
if [ $# -eq 0 ]; then
  echo "Debe proporcionar un argumento."
  exit 1
fi

# Obtener el primer argumento
argumento=$1

# Realizar diferentes acciones en función del argumento
case $argumento in
  "daily")
    python3 /home/dbmaker/app/main.py -t EVENTO FACSER MACTEL ORDREP SUCURSAL TURNOTAL VALECONS
    # Coloca aquí el código correspondiente a la acción 1
    ;;
  "monthly")
    python3 /home/dbmaker/app/main.py -t FACINT FACREF FACREP FAMCOD FAMTAREA HISTOTURNO LOGINES MOVTAR PLANCTA TECNICOS
    # Coloca aquí el código correspondiente a la acción 2
    ;;
  "2hour")
    python3 /home/dbmaker/app/main.py -t USADOS1 BUCFIN CLAAUTOS DEPOSITO PARMS
    # Coloca aquí el código correspondiente a la acción 2
    ;;
  "halfhour")
    python3 /home/dbmaker/app/main.py -t AUTOS AUTOS1 AUTOS8 AUTOS11 AUPPAGO BOLETO LOG_RESER MACLI1 MACTEL MARCAS RESERVA VENDE CTACTE SUCURSAL CONT INFDOM USADOS3
    # Coloca aquí el código correspondiente a la acción 2
    ;;
  *)
    echo "Argumento inválido.."
    exit 1
    ;;
esac
