@echo off 
rem call [1-8] for different view name

choice /C 12345678 /M "FDD_TDD_CA,CUE_Stability,CUE_stability2,CUE_ToT_4,CUE_TOT,CUE_TOT_2,mue_tot,sue_tot"
if errorlevel 8 goto yzheng_view_sue_tot_uk
if errorlevel 7 goto yzheng_view_mue_tot 
if errorlevel 6 goto yzheng_view_CUE_ToT_UK_2 
if errorlevel 5 goto yzheng_view_CUE_TOT_uk 
if errorlevel 4 goto yzheng_view_CUE_ToT_4
if errorlevel 3 goto yzheng_view_CUE_stability2 
if errorlevel 2 goto yzheng_CUE_Stability_view_uk 
if errorlevel 1 goto yzheng_CUE_FDD_TDD_CA_INT3 

:yzheng_CUE_FDD_TDD_CA_INT3
cd C:\Projects\yzheng_CUE_FDD_TDD_CA_INT3\tm_build_system\utilities
python remove_all_backup_files.pyw   
python remove_all_clearcase_files.pyw
python remove_all_derived_files.pyw  
goto end

:yzheng_CUE_Stability_view_uk
cd C:\Projects\yzheng_CUE_Stability_view_uk\tm_build_system\utilities
python remove_all_backup_files.pyw   
python remove_all_clearcase_files.pyw
python remove_all_derived_files.pyw  
goto end 
                  
:yzheng_view_CUE_stability2  
cd C:\Projects\yzheng_view_CUE_stability2\tm_build_system\utilities        
python remove_all_backup_files.pyw   
python remove_all_clearcase_files.pyw
python remove_all_derived_files.pyw 
goto end
      
:yzheng_view_CUE_ToT_4
cd C:\Projects\yzheng_view_CUE_ToT_4\tm_build_system\utilities
python remove_all_backup_files.pyw   
python remove_all_clearcase_files.pyw
python remove_all_derived_files.pyw
goto end

:yzheng_view_CUE_TOT_uk
cd C:\Projects\yzheng_view_CUE_TOT_uk\tm_build_system\utilities       
python remove_all_backup_files.pyw   
python remove_all_clearcase_files.pyw
python remove_all_derived_files.pyw  
goto end

:yzheng_view_CUE_ToT_UK_2
cd C:\Projects\yzheng_view_CUE_ToT_UK_2\tm_build_system\utilities   
python remove_all_backup_files.pyw   
python remove_all_clearcase_files.pyw
python remove_all_derived_files.pyw 
goto end

:yzheng_view_mue_tot
cd C:\Projects\yzheng_view_mue_tot\tm_build_system\utilities   
python remove_all_backup_files.pyw   
python remove_all_clearcase_files.pyw
python remove_all_derived_files.pyw  
goto end   

:yzheng_view_sue_tot_uk
cd C:\Projects\yzheng_view_sue_tot_uk\tm_build_system\utilities   
python remove_all_backup_files.pyw   
python remove_all_clearcase_files.pyw
python remove_all_derived_files.pyw           

:end
cd C:\Users\yzheng\Desktop        