#!/bin/bash

prompt="Choose a Server, or 'q' for quit"
ipRegex="[a-zA-Z\.]+@(([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})|([a-zA-Z\.\-]+))"
sshTimeout=2

printHelp() {
	echo "Usage: $0 <-d|-t|-p|-a> [-h]"
	echo "  -d : list development servers"
	echo "  -t : list test servers"
	echo "  -p : list production servers"
	echo "  -h : show help"
}

serverOptionsProd=(
	"-- PRODUCTION ------------------------------------------------------------------"
	"<username>@127.0.0.1 - Title"
	"..."
	"<username>@127.0.0.1 - Title" )

serverOptionsTest=(
	"-- TEST ------------------------------------------------------------------------"
	"<username>@127.0.0.1 - Title"
	"..."
	"<username>@127.0.0.1 - Title" )

serverOptionsDev=(
	"-- DEVELOPMENT -----------------------------------------------------------------"
	"<username>@127.0.0.1 - Title"
	"..."
	"<username>@127.0.0.1 - Title" )

serverOptionsInfra=(
	"-- INFRASTRUCTURE --------------------------------------------------------------"
	"<username>@127.0.0.1 - Title" 
	"..."
	"<username>@127.0.0.1 - Title" )
)

serverOptions=()

while getopts adtph option
do
	case "${option}"
		in
		a) 	serverOptions+=("${serverOptionsDev[@]}")
           		serverOptions+=("${serverOptionsTest[@]}")
           		serverOptions+=("${serverOptionsProd[@]}")
           		;;
		d) 	serverOptions+=("${serverOptionsDev[@]}")
			;;
		t) 	serverOptions+=("${serverOptionsTest[@]}")
			;;
		i)	serverOptions+=("${serverOptionsInfra[@]}")
			;;
		p) 	serverOptions+=("${serverOptionsProd[@]}")
			;;
		h) 	printHelp help; exit 0 
			;;
		*) 	printHelp ; exit 1 
			;;
	esac
done

if [ -z "${serverOptions[@]}" ] ; then
	echo "Parameter required."
	printHelp
	exit 1
fi

servers=()

function displayMenu() {
	clear
	printf "= SSH-INTO ========================================================================\n"
	counter=1
	for option in "${serverOptions[@]}" ; do
		if [[ $option =~ ^\-\-.*$ ]] ; then printf "\n$option\n\n" ;
		else 
			servers[counter-1]=$option
			printf "%4d - $option\n" $counter
			counter=$((counter+1))			
		fi
	done
	printf "\n-- OTHER -----------------------------------------------------------------------\n\n"
	printf "d) development\n"
	printf "t) test\n"
	printf "p) production\n"
	printf "i) infrastructure\n"
	printf "a) all\n"
	printf "n) new local shell\n"
	printf "\n--------------------------------------------------------------------------------\n"
	printf "\n$prompt > "
}

function choose() {	
	displayMenu

	read choice

	if [[ $choice =~ ^[nN]$ ]] ; then
		mintty &
	fi
	
	if [[ $choice =~ ^[tT]$ ]] ; then 
		serverOptions=("${serverOptionsTest[@]}")
	fi
	
	if [[ $choice =~ ^[dD]$ ]] ; then 
		serverOptions=("${serverOptionsDev[@]}")
	fi
	
	if [[ $choice =~ ^[pP]$ ]] ; then 
	        serverOptions=("${serverOptionsProd[@]}")
	fi

	if [[ $choice =~ ^[aA]$ ]] ; then 
		serverOptions=("${serverOptionsDev[@]}")
	        serverOptions+=("${serverOptionsTest[@]}")
        	serverOptions+=("${serverOptionsProd[@]}")
		serverOptions+=("${serverOptionsInfra[@]}")
	fi

	if [[ $choice =~ ^[iI]$ ]] ; then
		serverOptions=("${serverOptionsInfra[@]}")
	fi

	if [[ $choice =~ ^[0-9]+.*$ ]] ; then openServer $choice; fi
	if [[ $choice =~ ^[qQ].*$ ]] ; 	then return 1 ; fi

	return 0;
}

function openServer() {
	clear
	index=$(($1 - 1))
	length=${#servers[@]}
	if (( $index >= 0 )) && (( $index <= length)) ;	then
		arrayContent=${servers[$index]}
		if [[ $arrayContent =~ $ipRegex ]] ; then
			sshTarget="${BASH_REMATCH[0]}"
			printf "SSH > $sshTarget\n\n"
			mintty ssh -o ConnectTimeout=$sshTimeout $sshTarget &
			if [[ "$?" =~ "0" ]] ; then return; 
			else
				read
			fi
			pause
		else
			printf "Invalid choice [$arrayContent]..."
			pause
		fi		
	fi
}

function pause() {
	printf "\n\nPress any key to continue..."
			read -n1 ignored
}

while choose ; do 
	echo "..."
done 