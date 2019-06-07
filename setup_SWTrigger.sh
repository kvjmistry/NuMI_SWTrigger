source /grid/fermiapp/products/uboone/setup_uboone.sh;
setup uboonecode v06_26_01_13 -q e10:debug;
echo "Now enter Kinit and then kx509 if you havent already done so" ; 
echo "next get another proxy voms-proxy-init -noregen -rfc -voms fermilab:/fermilab/uboone/Role=Analysis"
