function numor_data = raw_read_ornl_sans(fname,numor)

%This is the data loader for ORNL CG2 SANS.

global inst_params

param = zeros(128,1);

result = parse_file(fname)

warning on

numor_data.info.start_date = ['**-**-**']; %Start Date
numor_data.info.start_time = ['**-**-**']; %Start Time
numor_data.info.end_date = ['**-**-**']; %End Date
numor_data.info.end_time = ['**-**-**']; %End Time
numor_data.info.user = ['NoName']; %User name


param(inst_params.vectors.reactor_power) = ''
numor_data.info.user = ''
numor_data.subtitle = ''
param(inst_params.vectors.det) = str2num(result.params.sample_detector_distance)+str2num(ORNL_offset)*0.001+str2num(int_off)*0.001; % in m


    if strfind(linestr,'<sample_to_flange ')
        temp1=findstr(linestr,'>'); temp2=findstr(linestr,'<');% Added by LDS 7/17/15
        ORNL_offset=linestr(temp1+1:temp2(2)-1); 
    end
    if strfind(linestr,'<tank_internal_offset ')
        temp1=findstr(linestr,'>'); temp2=findstr(linestr,'<');% Added by LDS 7/17/15
        int_off=linestr(temp1+1:temp2(2)-1);
    end
    
    if strfind(linestr,'<selector_speed ')
        temp1 = findstr(linestr,'>'); temp2 = findstr(linestr,'<');
        wav_str = linestr(temp1+1:temp2(2)-1);
        param(inst_params.vectors.wav) = 0.14858+(23761.9/str2num(wav_str)); % in Angs    
        
        %Check for zero value
        if param(inst_params.vectors.wav) ==0;
            temp =inputdlg(({'Enter Wavelength'}),'Wavelength Zero in File: Enter Wavelength',[1],{'6'});
            param(inst_params.vectors.wav) = str2num(temp{:});
        end
    end
    
    if strfind(linestr,'<wavelength_spread type=')
        temp1 = findstr(linestr,'>'); temp2 = findstr(linestr,'<');
        delta_wav_str = linestr(temp1+1:temp2(2)-1);
        param(inst_params.vectors.deltawav) = str2num(delta_wav_str); % in Angs
        
        %Check for zero value
        if param(inst_params.vectors.deltawav) ==0;
            temp =inputdlg(({'Enter Wavelength Spread'}),'Wavelength Spread Zero in File: Enter DLambda (%)',[1],{'6'});
            param(inst_params.vectors.deltawav) = str2num(temp{:})/100;
        end
    end
    
    
    if strfind(linestr,'<source_distance ')
        temp1 = findstr(linestr,'>'); temp2 = findstr(linestr,'<');
        col_str = linestr(temp1+1:temp2(2)-1);
        param(inst_params.vectors.col)=str2num(col_str)/1000;
    end
    
    if strfind(linestr,'<source_aperture_size')
        temp1 = findstr(linestr,'>'); temp2 = findstr(linestr,'<');
        source_str = linestr(temp1+1:temp2(2)-1);        
        param(inst_params.vectors.source_ap)=str2num(source_str)/1000;
    end

    if strfind(linestr,'<selector_speed ') %Selector speed RPM EB 07/08/11
        temp1 = findstr(linestr,'>'); temp2 = findstr(linestr,'<');
        temp_str = linestr(temp1+1:temp2(2)-1);
        param(inst_params.vectors.sel_rpm) = str2num(temp_str);
    end

    if strfind(linestr,'<beam_trap_x ') %Beam stop x EB 07/08/11
        temp1 = findstr(linestr,'>'); temp2 = findstr(linestr,'<');
        temp_str = linestr(temp1+1:temp2(2)-1);
        param(inst_params.vectors.bx) = str2num(temp_str);
    end
    
    if strfind(linestr,'<trap_y_76mm ') %Beam stop y EB 07/08/11
        temp1 = findstr(linestr,'>'); temp2 = findstr(linestr,'<');
        temp_str = linestr(temp1+1:temp2(2)-1);
        if temp_str >200
            param(inst_params.vectors.by) = str2num(temp_str);
        end
    end
    
    if strfind(linestr,'<trap_y_101mm ') %Beam stop y LDS 7/19/2015
        temp1 = findstr(linestr,'>'); temp2 = findstr(linestr,'<');
        temp_str = linestr(temp1+1:temp2(2)-1);
        if temp_str >200
            param(inst_params.vectors.by) = str2num(temp_str);
        end
    end
    
    if strfind(linestr,'<trap_y_25mm ') %Beam stop y LDS 7/19/2015
        temp1 = findstr(linestr,'>'); temp2 = findstr(linestr,'<');
        temp_str = linestr(temp1+1:temp2(2)-1);
        if temp_str >200
            param(inst_params.vectors.by) = str2num(temp_str);
        end
    end
    
    if strfind(linestr,'<trap_y_50mm ') %Beam stop y LDS 7/19/2015
        temp1 = findstr(linestr,'>'); temp2 = findstr(linestr,'<');
        temp_str = linestr(temp1+1:temp2(2)-1);
        if temp_str >200
            param(inst_params.vectors.by) = str2num(temp_str);
        end
    end
    
    if strfind(linestr,'<time ');
        temp1 = findstr(linestr,'>'); temp2 = findstr(linestr,'<');
        time_str = linestr(temp1+1:temp2(2)-1);
        param(inst_params.vectors.time) = str2num(time_str);
    end

    if strfind(linestr,'<tsample2 ') %Regulation temperature EB 07/08/11, Old configChanged by LDS 7/17/15
        temp1 = findstr(linestr,'>'); temp2 = findstr(linestr,'<');
        temp_str_samp2 = linestr(temp1+1:temp2(2)-1);
        param(inst_params.vectors.temp) = str2num(temp_str_samp2);
    end
    
   
    if strfind(linestr,'<tvti ') %New temp for Magnet Changed by LDS 7/17/15
        temp1 = findstr(linestr,'>'); temp2 = findstr(linestr,'<');
        temp_str_tvti = linestr(temp1+1:temp2(2)-1);
        param(inst_params.vectors.treg) = str2num(temp_str_tvti);
    end
    
    if strfind(linestr,'<tsample ')
        tvti_exist=exist('temp_str_tvti','var');
        if tvti_exist
            temp1 = findstr(linestr,'>'); temp2 = findstr(linestr,'<');
            temp_str_samp = linestr(temp1+1:temp2(2)-1);
            param(inst_params.vectors.temp) = str2num(temp_str_samp);
        else
            temp1 = findstr(linestr,'>'); temp2 = findstr(linestr,'<');
            temp_str_samp1 = linestr(temp1+1:temp2(2)-1);
            param(inst_params.vectors.treg) = str2num(temp_str_samp1);
        end
    end
    if strfind(linestr,'<chillerp ')
        temp1=findstr(linestr,'>'); temp2=findstr(linestr,'<');
        temp_str=linestr(temp1+1:temp2(2)-1);
        param(inst_params.vectors.temp) = str2num(temp_str)+273.15;
    end
    if strfind(linestr,'<monitor ')
        temp1 = findstr(linestr,'>'); temp2 = findstr(linestr,'<');
        monitor_str = linestr(temp1+1:temp2(2)-1);
        param(inst_params.vectors.monitor) = str2num(monitor_str);
    end

    if strfind(linestr,'sample_zarc ')     %zarc is d22 phi
        temp1 = findstr(linestr,'>'); temp2 = findstr(linestr,'<');
        zarc_str = linestr(temp1+1:temp2(2)-1);
        param(inst_params.vectors.zarc)=str2num(zarc_str);
    end

    if strfind(linestr,'sample_rotation ')
        temp1 = findstr(linestr,'>'); temp2 = findstr(linestr,'<');
        rot_str = linestr(temp1+1:temp2(2)-1);
        param(inst_params.vectors.san)=str2num(rot_str);
    end
    
    if strfind(linestr,'attenuator_pos ')
        temp1 = findstr(linestr,'"'); temp2 = findstr(linestr,'"');
        att_str = linestr(temp1+1:temp2(2)-1);
        if strcmp(att_str,'open'); att = 0; att_status = 0;
        elseif strcmp(att_str,'x2k'); att = 1; att_status = 1;
        else  att = 0; att_status = 0;
        end
        
        
        param(inst_params.vectors.att_type) = att;
        param(inst_params.vectors.att_status) = att_status;
        
        
    end


    

    if strfind(linestr,'<mag_current ') %Magnetic field
        temp1 = findstr(linestr,'>'); temp2 = findstr(linestr,'<');
        mag_str = linestr(temp1+1:temp2(2)-1);
        param(inst_params.vectors.field) = 372.95*(str2num(mag_str)-0.013)+15;
    end

    %
    %     if strfind(linestr,'<beam_center_x_pixel type="FLOAT32">')
    %         bx=strtok(linestr,'<beam_center_x_pixel type="FLOAT32">');
    %         param(inst_params.vectors.bx)=str2num(bx);
    %     end
    %
    %     if strfind(linestr,'<beam_center_y_pixel type="FLOAT32">')
    %         by=strtok(linestr,'<beam_center_y_pixel type="FLOAT32">');
    %         param(inst_params.vectors.by)=str2num(by);
    %     end

    %if strfind(linestr,'<Detector type="INT32[192,192]">')
    if strfind(linestr,'<Detector type="INT32') % EB 06/08/2011
        data=fscanf(fid,'%g',[inst_params.detector1.pixels(2) inst_params.detector1.pixels(1)]);
    end
end
 
%Close the data file
fclose(fid);

%Add extra parameter total counts actually counted from the data in the file
param(127) = sum(sum(data)); %The total Det counts as summed from the data array
param(128) = numor; %Additional parameter added by chuck
disp('Using SQRT(I) errors')
error_data = sqrt(data);

numor_data.data1 = data;
numor_data.error1 = error_data;
numor_data.params1 = param;














function result = parse_file(fileName)
f = fopen(fileName,'r');
while ~feof(f)               
    s = strtrim(fgetl(f));
    if isempty(s)
        % Data Section
        result.data=fscanf(f,'%g',[str2num(result.params.number_of_x_pixels) str2num(result.params.number_of_y_pixels)]);
        return;
    end;
    if (s(1)=='#')
        continue;
    end;
    if strfind(s,'=')
        [key,val] = strtok(s, '=');
        key = strrep(key, '-', '_');
        val = strtrim(val);
        if strcmpi(val(1),'=')
            val(1)=[];
        end
        result.params.(lower(genvarname(key))) = val;
    end
end
fclose(f);
return;


>> import test1.*  
>> result = test1('test.ini')           

result = 

    params: [1x1 struct]
      data: [192x256 double]

>> result.params                        

ans = 

                   aperture_distances: '1919.1,'
                        beam_diameter: '7.37512707557'
                   beam_trap_diameter: '76.2'
                        beam_center_x: '22.2014452187'
                        beam_center_y: '121.006975959'
    default_incident_monitor_spectrum: '1.0'
      default_incident_timer_spectrum: '2.0'
             detector_distance_offset: '711.0'
                        detector_name: 'detector1'
                              monitor: '9458973.0'
                     number_of_guides: '5'
                   number_of_monitors: '2.0'
                   number_of_x_pixels: '192.0'
                   number_of_y_pixels: '256.0'
                            run_start: '2015-08-06 02:33:45'
                            run_title: 'P1 S S1 Side 1m4.75A5g'
             sample_aperture_diameter: '2.0'
             sample_detector_distance: '1802.5'
                     sample_thickness: '0.0'
             source_aperture_diameter: '20.0'
               source_sample_distance: '7377.5'
                           start_time: '2015-08-06 02:33:45'
                                timer: '2700.0'
                           wavelength: '4.86'
                    wavelength_spread: '0.13'
                         x_pixel_size: '5.5'
                         y_pixel_size: '4.3'

>> 
