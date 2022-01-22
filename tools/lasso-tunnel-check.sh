#!/bin/bash
if [[ -n $(netstat -l | grep $1) ]]; then 
	echo "Tunnel $1 is up!"
else
	echo "Tunnel $1 is down."	
fi
