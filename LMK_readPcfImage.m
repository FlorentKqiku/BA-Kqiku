function XYZ = LMK_readPcfImage(dir_name)
%AUTHOR: Frederic Rudawski TU Berlin, FG Lichttechnik,
%	frederic.rudawski@campus.tu-berlin.de, www.li.tu-berlin.de
% based on LMK_readPfImage of  Jan Winter, Sandy Buschmann, Robert Franke, TU Berlin, FG Lichttechnik
%
% LICENSE: free to use at your own risk. Kudos appreciated.
%
%   Reads the data from a LMK .pcf File and returns the values of the
%   luminosity image
    % 
    % Input:
    % path to file
    %
    % Output:
    % luminanceColorImage = XYZ array of dimension lines-by-columns (single)
    

%read data from given filePath
try
    [fid, message] = fopen(dir_name,'r');
    disp(message);
catch
    [file,path] = uigetfile('*.pcf','Select luminance color .pcf image');
    if isequal(file,0)
        XYZ = [];
        return
    end
    [fid, message] = fopen([path file],'r');
    disp(message);
end

% try
    %read header
    fseek(fid, 48, 'cof');
    lines = str2double(fread(fid, [1 , 4], '*char'));
    fseek(fid, 10, 'cof');
    columns = str2double(fread(fid, [1, 4], '*char'));

    totalNumberOfBytes = lines*columns*12; % .pcf-format has 4 Bytes per pixel for each channel R G B.
    
    % initialize:
    %luminanceImage = zeros(lines*columns, 4);
    
    % write into array:
    fseek(fid, -totalNumberOfBytes, 'eof');
    im = fread(fid, inf, '*float');

fclose(fid);
    
    % luminanceImage is a (columns*lines)-by-3 matrix; reshape into colums-by-lines
    % matrix:    
    l = length(im);
    l = floor(l / lines) * lines;
    im = im(1:l);
    luminanceImageS = reshape(im, [], lines)';
    im = luminanceImageS;

% catch
%     disp(lasterror.message)
%     disp(lasterror.stack)
%     feof(fid)
%     fclose(fid);
% end

% create color image matrix
RGB = zeros(lines,columns,3);
RGB(:,:,3) = flipud(im(:,1:3:end));
RGB(:,:,2) = flipud(im(:,2:3:end));
RGB(:,:,1) = flipud(im(:,3:3:end));

% RGB to XYZ transformation
% from: Colorimetry - fundamentals and applications, authors: Robertson and Ohta on page 70
XYZ = zeros(lines,columns,3);
XYZ(:,:,1) = 2.7689.*RGB(:,:,1) + 1.7517.*RGB(:,:,2) + 1.1302.*RGB(:,:,3);
XYZ(:,:,2) = 1.0000.*RGB(:,:,1) + 4.5907.*RGB(:,:,2) + 0.0601.*RGB(:,:,3); % luminance matrix
XYZ(:,:,3) = 0.0000.*RGB(:,:,1) + 0.0565.*RGB(:,:,2) + 5.5943.*RGB(:,:,3);

% function end
end