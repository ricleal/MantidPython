function numor_data = raw_read_ornl_sans(fname,numor)

%This is the data loader for ORNL CG2 SANS.

% Ricardo Edits
% Parses the files
result = parse_file(fname);
% Metadata
disp('*** Metadata');
disp(result.params);
% Data 
disp('*** Data')
disp(size(result.data))
% 

global inst_params
param = zeros(128,1);

warning on

numor_data.info.start_date = ['**-**-**']; %Start Date
numor_data.info.start_time = ['**-**-**']; %Start Time
numor_data.info.end_date = ['**-**-**']; %End Date
numor_data.info.end_time = ['**-**-**']; %End Time
numor_data.info.user = ['NoName']; %User name



param(inst_params.vectors.reactor_power) = str2num(result.params.header_reactor_power);
numor_data.info.user = result.params.header_users
numor_data.subtitle = result.params.header_scan_title
param(inst_params.vectors.det) = str2num(result.params.motor_positions_sample_det_dist)+str2num(result.params.header_sample_to_flange)*0.001+str2num(result.params.header_tank_internal_offset)*0.001; % in m

%
% TODO: Complete the rest!
%

%Add extra parameter total counts actually counted from the data in the file
param(127) = sum(sum(result.data)); %The total Det counts as summed from the data array
param(128) = numor; %Additional parameter added by chuck
disp('Using SQRT(I) errors')
error_data = sqrt(result.data);

numor_data.data1 = result.data;
numor_data.error1 = error_data;
numor_data.params1 = param;

function result = parse_file(fileName)
f = fopen(fileName,'r');
while ~feof(f)               
    s = strtrim(fgetl(f));
    if isempty(s)
        % Data Section
        result.data=fscanf(f,'%g',[str2num(result.params.number_of_y_pixels) str2num(result.params.number_of_x_pixels) ]);
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
        end;
%        [x, status] = str2num(val);
%        if status
%            val = x;
%        end;
        result.params.(lower(genvarname(key))) = val;
    end;
end;
fclose(f);
return;
