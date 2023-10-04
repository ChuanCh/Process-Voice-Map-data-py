vrp_folder = 'L:\Huanchen\Thyrovoice\Py_VRP\group_by_sur_type\group_by_pres_and_posts\Total';
save_folder = 'L:\Huanchen\Thyrovoice\Py_VRP\group_by_sur_type\group_by_pres_and_posts\Total\Album';
% Check if save_folder exists
if ~exist(save_folder, 'dir')
    % If it doesn't exist, create it
    mkdir(save_folder);
end
extension = '*.csv';  % for .mat files
vrp_files = dir(fullfile(vrp_folder, extension));
vrp_files = vrp_files(~strcmp({vrp_files.name}, 'centroids.csv'));
VRP = [];
% Counter for subplots
plotCounter = 1;

% Initialize a new figure
f = figure;
f.Position = [10 10 800 1800];
tiledlayout(4,2, 'Padding', 'none', 'TileSpacing', 'compact');

for i=1:length(vrp_files)
    file_name = vrp_files(i).name;
    vrp_file = fullfile(vrp_folder, file_name);
    [names, vrp] = FonaDynLoadVRP(vrp_file);
    vrp_title = strrep(file_name(1:15), '_', ' ');
    mSymbol = FonaDynPlotVRP(vrp, names, 'maxCluster', subplot(4, 2, plotCounter), 'ColorBar', 'on','PlotHz', 'off', 'MinCycles', 1);  
    pbaspect([1.5 1 1]);
    xlabel('midi');
    ylabel('dB');
    grid on
    subtitle(string(vrp_title));

    % If 8 plots are reached or end of files, reset counter and create a new figure
    if plotCounter == 8 || i == length(vrp_files)
        plotCounter = 1;
        % save as pdfs
        pdf_name = file_name(1:6);
        sgtitle(pdf_name);
        pdf_file = fullfile(save_folder, pdf_name);
        set(gcf,'PaperOrientation','portrait');
        set(gcf, 'PaperSize', [30, 40]);
        print(gcf, pdf_file,'-dpdf','-r600', '-bestfit');
        close gcf
        if i ~= length(vrp_files)
            f = figure;
            f.Position = [10 10 800 1800];
            tiledlayout(4,2, 'Padding', 'none', 'TileSpacing', 'compact');
        end
    else
        plotCounter = plotCounter + 1; 
    end
end