cd lightgbm_dart_noextratree;
sh run.sh;
cd ..;
echo "lightgbm_dart_noextratree finish;"

cd lightgbm_dart_extratree;
sh run.sh;
cd ..;
echo "lightgbm_dart_extratree finish;"

cd lightgbm_gbdt_noextratree;
sh run.sh;
cd ..;
echo "lightgbm_gbdt_noextratree finish;"

cd lightgbm_gbdt_extratree;
sh run.sh;
cd ..;
echo "lightgbm_gbdt_extratree finish;"

cd lightgbm_gbdt_extratree;
sh run.sh;
cd ..;
echo "lightgbm_gbdt_extratree finish;"

cd lightgbm_rf_noextratree;
sh run.sh;
cd ..;
echo "lightgbm_rf_noextratree finish;"

# shellcheck disable=SC2164
cd lightgbm_rf_extratree;
sh run.sh;
cd ..;
echo "lightgbm_rf_extratree finish;"

cd lightgbm_goss_noextratree;
sh run.sh;
cd ..;
echo "lightgbm_goss_noextratree finish;"

cd lightgbm_goss_extratree;
sh run.sh;
cd ..;
echo "lightgbm_goss_extratree finish;"
