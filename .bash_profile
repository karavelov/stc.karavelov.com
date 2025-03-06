clear
source /var/www/karavelov/stc/env_site/bin/activate
cd /var/www/karavelov/stc/

echo -e "\e[32m"
figlet -f big "Welcome to"
figlet -f big -w 200 "Smart Traffic Control"
figlet -f standard -w 200 "www . stc . karavelov . com"

echo -e "\e[0m"

export PS1="\[\e[32m\]SmartTrafficControl \u$\[\e[0m\] "

. "$HOME/.cargo/env"
