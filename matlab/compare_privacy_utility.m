function compare_privacy_utility(summary_csv, output_file)
% Plot the privacy-utility curve exported from repeated Python experiments.
if nargin < 1
    summary_csv = fullfile('..', 'results', 'privacy_utility.csv');
end
if nargin < 2
    output_file = fullfile('..', 'results', 'matlab_privacy_utility.png');
end
summary = readtable(summary_csv);
figure('Color', 'w');
plot(summary.epsilon, summary.f1, '-o', 'LineWidth', 1.5);
xlabel('Approximate privacy budget epsilon');
ylabel('F1 score');
title('Privacy-utility trade-off');
grid on;
exportgraphics(gcf, output_file, 'Resolution', 220);
end
