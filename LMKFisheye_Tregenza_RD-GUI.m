% LOAD .PF FILE(S) AND COMPUTE L, Ev, x AND y FROM EACH TREGENZA REGION.
%
% Only for .pf images of the nivil LMK with fisheye
%
% The viewing angle for the L-explosion can be altered by changing azimuth
% and elevavation in the beginning of the script. You can alternatively
% change the the view in the Matlab figure window and export it from there.
%
% Please note: The lowest almucantar band is not completely covered.
% Also: You should not switch between Matlab figure windows, for the
% plotting will appear in the current window.
%
% Author: Frederic Rudawski
% Date: 31.08.2017
%
% -------------------------------------------------------------------------------
% Date: 11.10.2021
% Updated for the Purpose of a Python GUI in the Bachelor Thesis of Florent Kqiku
% Small changes have been made so the Matlab script is calleble from Python
% The pf. Images are goin to be loaded through the GUI and given in this Script as Arguments
% The Results are goin to be saved in a folder created in the same location as the loaded pf. images
% A .png of the calculated Directogram is goin to be shown on the GUI aswell
% Other then that no changes are been made.
%
% Usage: Just start the Python file "image_prozessing" and than choose the directogram checkbox
%        after selecting the .pf pictures
%
% Update-Author: Florent Kqiku
% -------------------------------------------------------------------------------




function LMKFisheye_Tregenza(file, pathfile)

    % viewing angles
    azimuth = 0;
    elevation = -90;



    % Trengenza regions
    %rho = [0 45 45 60];
    %phi = {[0 35 35 145 145 180],[0 35 35 145 145 180]};

    rho = [0 6 6 18 18 30 30 42 42 54 54 66 66 78 78 90]; % radius distance in degree
    phi = {[0 360],...
           [0 60 60 120 120 180 180 240 240 300 300 360],...
           [15 45 45 75 75 105 105 135 135 165 165 195 195 225 225 255 255 285 285 315 315 345 345 15]...
           [0 20 20 40 40 60 60 80 80 100 100 120 120 140 140 160 160 180 180 200 200 220 220 240 240 260 260 280 280 300 300 320 320 340 340 360]...
           [7.5 22.5 22.5 37.50 37.5 52.5 52.5 67.5 67.5 82.5 82.5 97.5 97.5 112.5 112.5 127.5 127.5 142.5 142.5 157.5 157.5 172.5 172.5 187.5 187.5 202.5 202.5 217.5 217.5 232.5 232.5 247.5 247.5 262.5 262.5 277.5 277.5 292.5 292.5 307.5 307.5 322.5 322.5 337.5 337.5 352.5 352.5 7.5]...
           [7.5 22.5 22.5 37.50 37.5 52.5 52.5 67.5 67.5 82.5 82.5 97.5 97.5 112.5 112.5 127.5 127.5 142.5 142.5 157.5 157.5 172.5 172.5 187.5 187.5 202.5 202.5 217.5 217.5 232.5 232.5 247.5 247.5 262.5 262.5 277.5 277.5 292.5 292.5 307.5 307.5 322.5 322.5 337.5 337.5 352.5 352.5 7.5]...
           [0 12 12 24 24 36 36 48 48 60 60 72 72 84 84 96 96 108 108 120 120 132 132 144 144 156 156 168 168 180 180 192 192 204 204 216 216 228 228 240 240 252 252 264 264 276 276 288 288 300 300 312 312 324 324 336 336 348 348 360],...
           [0 12 12 24 24 36 36 48 48 60 60 72 72 84 84 96 96 108 108 120 120 132 132 144 144 156 156 168 168 180 180 192 192 204 204 216 216 228 228 240 240 252 252 264 264 276 276 288 288 300 300 312 312 324 324 336 336 348 348 360]}; % counter clockwise angle
    %}

    % color
    tclr = [0.9 0.1 0.45];
    % label font size
    labelfontsize = 4;


    % Tregenza patchnumbers
    patchnumber = [145 141 142 143 144 139 140 134:-1:127 138:-1:135 114:126 109:113 101:-1:85 108:-1:102 68:84 61:67 52:-1:31 60:-1:53 9:30 1:8];

    rho(rho==0) = 0.001;

    %[file,path] = uigetfile('*.pf','load luminance image','Multiselect','on');
    %file = getfile;
    %path = getpath;

    if sum(size(file)) == 2
        disp([10,'Aborted by user.',10])
        return
    end
    om = LMK_readPfImage(['OmegaImage_FishEyeLens.pf']);
    om = flipud(om);
    om = om(:,2:end-1);
    theta = LMK_readPfImage(['ThetaImage_FishEyeLens.pf']);
    theta = flipud(theta);
    theta = theta(:,2:end-1);
    omdata = om';
    omdata = omdata(:);
    thetadata = theta';
    thetadata = thetadata(:);

    loopend = size(file,2);



    % loop over files
    for image = 1:loopend

        patchL = zeros(1,145);
        patchE = zeros(1,145);
        ind = 1;
        area = [];
        figure
        % read image
        try
            im = LMK_readPfImage([pathfile{image}]);
            %im = flipud(im);
            im = im(2:end-1,:);
            filename = file{image}(1:end-2);

        catch
            im = LMK_readPfImage(pathfile);
            %im = flipud(im);
            %im = im(2:end-1,:);
            im = im(:,2:end-1);
            filename = file(1:end-2);
            loopend = 1;
        end
        clf
        imdata = im';
        imdata = imdata(:);
        % plot image
        try
            LMK_plotPcfImage(im);
        catch
            h = contourf(flipud(im),'EdgeColor','none');
            colorbar
        end
        axis equal
        a = [630 2000 200 1530];
        %axis(a)
        drawnow

        % save empty image
        path = erase(pathfile, file);
        path = path(1:end-1);
        folderToCreate = [filename(1:end-1) ' - Directogram'];
        mkdir(path, folderToCreate);
        folderPath = [path '/' folderToCreate '/'];
        
        print(gcf,'-dpng','-r300', [folderPath filename(1:end-1) '-empty.' 'png']);

        % center point
        [y0,x0] = find(theta==0);
        y0 = y0(1);
        x0 = x0(1);

        hold on


        % index for areas
        areaindex = 1;

        r_section = 1;
        test_E = 0; % for testimg E_v,sum
        % loop sections
        for s = 1:2:size(rho,2)-1

            % invisible contour plot for correct region coordinates
            inv = figure('Visible','Off');
            c0 = contour(theta,[0 rho(s)+(rho(s+1)-rho(s))/2]);
            c1 = contour(theta,[0 rho(s)]);
            c2 = contour(theta,[0 rho(s+1)]);
            c0 = c0(:,2:end);
            c1 = c1(:,2:end);
            c2 = c2(:,2:end);
            close(inv);

            % a complex way to get correct region coordinates from theta pf image
            [p1,~] = cart2pol(c1(1,2:end)'-x0,c1(2,2:end)'-y0);
            p1 = p1./(pi/180)+180;
            [p1,i1] = sort(p1);
            cor1 = [];
            if ~isempty(c1)
                cor1(1,:) = c1(1,i1);
                cor1(2,:) = c1(2,i1);
            end
            [p2,~] = cart2pol(c2(1,2:end)'-x0,c2(2,2:end)'-y0);
            p2 = p2./(pi/180)+180;
            [p2,i2] = sort(p2);
            cor2 = [];
            cor2(1,:) = c2(1,i2);
            cor2(2,:) = c2(2,i2);

            % circle of label coordinates candidates
            [p0,~] = cart2pol(c0(1,2:end)'-x0,c0(2,2:end)'-y0);
            p0 = p0./(pi/180)+180;
            [p0,i0] = sort(p0);
            cor0 = [];
            cor0(1,:) = c0(1,i0);
            cor0(2,:) = c0(2,i0);

            for j = 1:2:size(phi{r_section},2)-1


                [~, ind1] = min(abs(p1-phi{r_section}(j)));
                [~, ind2] = min(abs(p1-phi{r_section}(j+1)));
                [~, ind3] = min(abs(p2-phi{r_section}(j)));
                [~, ind4] = min(abs(p2-phi{r_section}(j+1)));

                % inner coordinates
                if ~isempty(cor1)
                    xp1 = cor1(1,min(ind1,ind2):max(ind1,ind2));
                    yp1 = cor1(2,min(ind1,ind2):max(ind1,ind2));
                else
                    xp1 = [];
                end
                % outer coordinates
                xp2 = cor2(1,min(ind3,ind4):max(ind3,ind4));
                yp2 = cor2(2,min(ind3,ind4):max(ind3,ind4));


                % best fitting label coordinates
                labelphi = phi{r_section}(j)+(phi{r_section}(j+1)-phi{r_section}(j))/2;
                [~,label_ind] = (min(abs(p0-labelphi)));
                labelx = cor0(1,label_ind);
                labely = cor0(2,label_ind);


                % over 360 degree
                if phi{r_section}(j+1) < phi{r_section}(j)
                    xp1 = [cor1(1,max(ind1,ind2):end) cor1(1,1:min(ind1,ind2))];
                    xp2 = [cor2(1,max(ind3,ind4):end) cor2(1,1:min(ind3,ind4))];
                    yp1 = [cor1(2,max(ind1,ind2):end) cor1(2,1:min(ind1,ind2))];
                    yp2 = [cor2(2,max(ind3,ind4):end) cor2(2,1:min(ind3,ind4))];
                    labelx = cor0(1,end);
                    labely = cor0(2,end);
                end


                if ~isempty(xp1)
                    patchx = [xp1(1) xp2 xp1(end) fliplr(xp1) xp1(1)];
                    patchy = [yp1(1) yp2 yp1(end) fliplr(yp1) yp1(1)];
                else
                    patchx = xp2;
                    patchy = yp2;
                end

                % circle center ?
                if phi{r_section}(1) == 0 && phi{r_section}(2) == 360
                    patchx = xp2;
                    patchy = yp2;
                    labelx = x0;
                    labely = y0;
                end



                % plot region borders
                area(areaindex) = patch(patchx,patchy,[1 1 1],'FaceColor','none','EdgeColor',tclr);
                drawnow

                % find pixels in region
                yin = 1:size(im,1);
                xin = 1:size(im,2);
                [y,x] = meshgrid(yin,xin);
                xdata = x(:);
                ydata = y(:);
                inside = inpolygon(xdata,ydata,patchx,patchy);

                % create inside Matrix
                Minside = zeros(size(im'));
                Minside(inside) = 1;
                Minside = Minside';

                % testing inside Matrix masking
                %{
                figure
                contourf(Minside.*im,'EdgeColor','none')
                hold on
                patch(patchx,patchy,[1 1 1],'FaceColor','none','EdgeColor','k');
                %plot(ydata(inside),xdata(inside),'r.')
                axis equal
                figure(1)
                %}

                % Pixels in region
                L = im.*Minside;
                E = im.*Minside.*cosd(theta).*om;
                Lr = sum(sum(L))/(size(inside(inside==1),1));
                Ev = sum(sum(E));

                % add labels to region
                text(labelx,labely,[num2str(round(Ev*10)/10),' lx',10,num2str(round(Lr*10)/10),' cd/m^2'],'HorizontalALignment','Center','VerticalAlignment','middle','FontSize',labelfontsize,'Color',tclr)

                patchL(1,patchnumber(ind)) = Lr;
                patchE(1,patchnumber(ind)) = Ev;

                areaindex = areaindex+1;
                test_E = test_E + Ev;


                ind = ind+1;
            end
            r_section = r_section + 1;
        end

        % Ev_ges calculation
        Ev_ges = sum(sum((om.*im.*cosd(theta))));
        text(1825,300,['E_{v,sum} = ',num2str(round(Ev_ges*10)/10),' lx'],'HorizontalAlignment','Center','Fontsize',labelfontsize,'Color',tclr)

        % refresh image
        drawnow
        % save image
        print(gcf,'-dpng','-r300', [folderPath filename 'png']);




        hold off
        axis equal
        grid on
        %axis([-2 2 -2 2 0 2])
        axis off




        % EXPLOSION PLOT

        figure

        % Tregenza table
        tt = [1 30 6 12; 2 30 18 12; 3 24 30 15; 4 24 42 15; 5 18 54 20; 6 12 66 30; 7 6 78 60; 8 1 90 0];
        % patch numbers and angles
        % line 1: almucantars
        % line 2: azimuths
        % line 3: Patchnumber
        pnt = [6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 18 18 18 18 18 18 18 18 18 18 18 18 18 18 18 18 18 18 18 18 18 18 18 18 18 18 18 18 18 18 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 42 42 42 42 42 42 42 42 42 42 42 42 42 42 42 42 42 42 42 42 42 42 42 42 54 54 54 54 54 54 54 54 54 54 54 54 54 54 54 54 54 54 66 66 66 66 66 66 66 66 66 66 66 66 78 78 78 78 78 78 90;180 192 204 216 228 240 252 264 276 288 300 312 324 336 348 0 12 24 36 48 60 72 84 96 108 120 132 144 156 168 168 156 144 132 120 108 96 84 72 60 48 36 24 12 0 348 336 324 312 300 288 276 264 252 240 228 216 204 192 180 180 195 210 225 240 255 270 285 300 315 330 345 0 15 30 45 60 75 90 105 120 135 150 165 165 150 135 120 105 90 75 60 45 30 15 0 345 330 315 300 285 270 255 240 225 210 195 180 180 200 220 240 260 280 300 320 340 0 20 40 60 80 100 120 140 160 150 120 90 60 30 0 330 300 270 240 210 180 180 240 300 0 60 120 NaN;1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145];

        plot_rgb = 0;
        % plot explosion
        L = patchL;
        hold on
        width = 5;
        width = 90-width;
        axis([0 1 0 1 0 1])
        % normalize L
        f = L./max(L);
        r = 1;
        els = 6;
        hold on
        if plot_rgb == 1
            clr = CLR;
        else
            clr = [f' f' f'];
        end
        for al = 1:size(tt,1)-1
            % plot almucantar
            ps = 0;
            for P = 1:tt(al,2)
                az = -deg2rad(ps-90);
                el = deg2rad(els);

                % patchnumber
                pp = find(pnt(1,:)==tt(al,3));
                p  = find(pnt(2,pp)==ps);
                patchn = pnt(3,pp(p));

                [x,y,z] = sph2cart(-az,el,f(patchn));
                if L(patchn)>0 && ~isnan(clr(patchn,1))
                    c = clr(patchn,:);
                else
                    c = [1 0 0];
                end

                line = plot3([0 x],[0 y],[0 z],'-','Color',[0.35 0.35 0.35],'LineWidth',0.5);

                Phi = deg2rad(linspace(0,360,101));
                Theta = deg2rad(ones(1,101).*width);
                [x,y,z] = sph2cart(Phi,Theta,f(patchn));
                face = fill3(x,y,z,c);
                set(face,'EdgeColor',[0.35 0.35 0.35])
                rotate(face,[0 1 0],90-rad2deg(el),[0 0 0]);
                rotate(face,[0 0 1],rad2deg(-az),[0 0 0]);

                ps = ps+tt(al,4);
            end
            els = els + 12;
        end
        % zenith
        az = deg2rad(0);
        el = deg2rad(90);
        [x,y,z] = sph2cart(az,el,f(145));
        line = plot3([0 x],[0 y],[0 z],'Color',[0.35 0.35 0.35]);

        Phi = deg2rad(linspace(0,360,101));
        Theta = deg2rad(ones(1,101).*width);
        [x,y,z] = sph2cart(Phi,Theta,f(145));
        face = fill3(x,y,z,c);
        set(face,'EdgeColor',[0.35 0.35 0.35])
        title('')
        axis  auto

        % set North arrow
        %plot3([0 0],[0 0.95],[0 0],'k')
        %plot3([-0.05 0 0.05],[0.90 0.95 0.90],[0 0 0],'k')
        %text(0,1.05,0,'N','HorizontalAlignment','center','FontSize',12)

        % GLOBUS

        % circle
        a = axis;
        c = 10/1.5;

        width = max([abs(a(2)) abs(a(3))])*1.45/10;
        Phi = deg2rad(linspace(0,360,101));
        Theta = deg2rad(ones(1,101).*width);
        [x,y,z] = sph2cart(Phi,Theta,width);

        %ax(2)=axes;
        %axis equal
        %axis off
        %axis(a)
        %hold on

        g1 = plot3(x,y,z,'Color',[0.55 0.55 0.55],'LineWidth',0.5);
        g2 = plot3(x,y,z,'Color',[0.55 0.55 0.55],'LineWidth',0.5);
        g3 = plot3(x,y,z,'Color',[0.55 0.55 0.55],'LineWidth',0.5);
        rotate(g2,[0 1 0],90,[0 0 0]);
        rotate(g3,[1 0 0],90,[0 0 0]);
        g1.XData = g1.XData+width*c;
        g2.XData = g2.XData+width*c;
        g3.XData = g3.XData+width*c;
        g1.YData = g1.YData-width*c;
        g2.YData = g2.YData-width*c;
        g3.YData = g3.YData-width*c;
        [x,y,z] = sphere(50);
        globus = surf(x.*width+width*c, y.*width-width*c, z.*width);
        globus.EdgeColor = 'none';
        colormap(gray)
        %shading interp

        %set(globus, 'FaceColor', [0.9 0.9 0.9]);
        % Nord arrow
        f = 2;
        plot3([0 0]+width*c,[-f*width f*width]-width*c,[0 0],'Color',[0.55 0.55 0.55],'LineWidth',0.5)
        plot3([0 0]+width*c,[0 0]-width*c,[-f*width f*width],'Color',[0.55 0.55 0.55],'LineWidth',0.5)
        plot3([-f*width f*width]+width*c,[0 0]-width*c,[0 0],'Color',[0.55 0.55 0.55],'LineWidth',0.5)

        % arrowhead
        %{
        [x,y,z] = cylinder([1 0],50);
        z = z*1.5;
        x = x.*width/5;
        y = y.*width/5;
        z = z.*width/5;
        cyl = surf(x+width*c,y-width*c,z+f.*width);
        cyl.EdgeColor = 'none';
        set(cyl, 'FaceColor', [0.55 0.55 0.55]);

        cyl = surf(x,y,z);
        z = z*1.5;
        cyl.EdgeColor = 'none';
        set(cyl, 'FaceColor', [0.55 0.55 0.55]);
        rotate(cyl,[1 0 0],-90,[0 0 0]);
        cyl.XData = cyl.XData+width*c;
        cyl.YData = cyl.YData-width*c+f.*width;
        %}
        %{
        cyl = surf(x,y,z);
        cyl.EdgeColor = 'none';
        set(cyl, 'FaceColor', [0.35 0.35 0.35]);
        rotate(cyl,[0 1 0],90,[0 0 0]);
        cyl.XData = cyl.XData+width*10/2+f.*width;
        cyl.YData = cyl.YData-width*10/2;
        %}


        %camlight
        %light('Position',[1 0 0],'Style','infinite');

        text(width*c,-width*c+1.25*f.*width,0,'Nadir','HorizontalAlignment','Center','VerticalAlignment','middle','Color',[0 0 0])
        text(width*c,-width*c,1.25*f.*width,'Center','HorizontalAlignment','Center','VerticalAlignment','middle','Color',[0 0 0])
        text(width*c,-width*c-1.25*f.*width,0,'Zenit','HorizontalAlignment','Center','VerticalAlignment','middle','Color',[0 0 0])

        axis equal
        axis off
        view([azimuth elevation])

        print(gcf,'-dpng','-r300', [folderPath filename(1:end-1) '1-explosion.' 'png']);

        h = get(gca,'Children');
        rotate(h,[0 -1 0],90)

        print(gcf,'-dpng','-r300', [folderPath filename(1:end-1) '2-explosion.' 'png']);


        % export  excel
        data = table((1:145)', patchL', patchE','VariableNames',{'patch','L','Ev'});
        try
            writetable(data,[folderPath filename(1:end-1) '.xls'])
        catch        
            fileID = fopen([folderPath filename 'txt'],'wt');
            %fprintf(fileID,'%Ev = 6.4f lx\n\n',Ev_ges);
            fprintf(fileID,['patch;    L;   E;\n']);
            %fprintf(fileID,'Ev      L_mean\n');
            for i = 1:145
                fprintf(fileID,'%u; %6.3f; %6.3f;\n',i, patchL(i), patchE(i));
            end
            % close txt file
            fclose(fileID);
        end

        % check if loop ending changed
        if loopend ~= 1
            display([num2str(image),' of ',num2str(loopend),' images done.'])
            %test_E
        else
            display('Image analysis done.')
            %test_E
            return
        end
    end
    

    display('Image analysis done.')
