function plot_trust_results(results_dir)
% Read CareFed exported CSV files and render research figures.
if nargin < 1
    results_dir = fullfile('..', 'results');
end
metrics = readtable(fullfile(results_dir, 'metrics.csv'));
gaps = readtable(fullfile(results_dir, 'group_gap_summary.csv'));
figure('Color', 'w');
bar(categorical(gaps.attribute), [gaps.positive_rate_gap gaps.recall_gap gaps.f1_gap]);
ylabel('Observed group gap');
title('CareFed trustworthiness audit');
legend({'Positive rate','Recall','F1'}, 'Location', 'northoutside');
grid on;
exportgraphics(gcf, fullfile(results_dir, 'matlab_group_gaps.png'), 'Resolution', 220);
fprintf('F1: %.4f\n', metrics.f1(1));
end
