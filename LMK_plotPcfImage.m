function LMK_plotPcfImage(im)
% Plot LMK .pcf image function
%
% Author: Frederic Rudawski
% Date: 19.07.2017
%
% The function makes a simple image adjustment for plotting. A better
% solution would be a HDR image creation. 
%
% For the image adjustment a factor  between the mean and max
% value of the image matrix is calculated. 

try 
    dummy = im;
    clear dummy
catch
    [file,path] = uigetfile('*.pcf','Select luminance color .pcf image');
    if isequal(file,0)
        return
    end
    im = LMK_readPcfImage([path file]);
end
% image adjustment factor
f1 = mean(mean(mean(im)));
f2 = max(max(max(im)));
f = mean([log10(f1) log10(f2)]);
f = 10^(f);
% primitive image adjustment
im = log10(im./f.*20);


% show image
if size(im,3) == 3
    % color
    image(real(flipud(im)));
else
    % grayscale
    imshow(im);
end

axis off
axis equal

end