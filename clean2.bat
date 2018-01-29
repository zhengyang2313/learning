@echo off 
rem call with the view name as the first parameter

cd C:\Projects\%1\tm_build_system\utilities
python remove_all_backup_files.pyw   
python remove_all_clearcase_files.pyw
python remove_all_derived_files.pyw         


cd C:\Users\yzheng\Desktop        