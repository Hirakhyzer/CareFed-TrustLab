function friedman_aggregation_test(repeated_csv)
% Compare F1 scores for aggregation methods across repeated seeds.
if nargin < 1
    repeated_csv = fullfile('..', 'results', 'repeated_aggregation_metrics.csv');
end
T = readtable(repeated_csv);
methods = unique(string(T.aggregation), 'stable');
seeds = unique(T.seed, 'stable');
values = nan(numel(seeds), numel(methods));
for i = 1:numel(methods)
    for j = 1:numel(seeds)
        x = T.f1(string(T.aggregation) == methods(i) & T.seed == seeds(j));
        if ~isempty(x)
            values(j, i) = x(1);
        end
    end
end
if any(isnan(values), 'all')
    error('Each aggregation method needs one F1 value per seed.');
end
[p, table_stats, stats] = friedman(values, 1, 'off');
fprintf('Friedman p-value: %.6f\n', p);
disp(table_stats);
pairs = multcompare(stats, 'Display', 'off');
pair_table = array2table(pairs, 'VariableNames', {'MethodA','MethodB','LowerCI','Difference','UpperCI','pValue'});
pair_table.MethodA = methods(pair_table.MethodA);
pair_table.MethodB = methods(pair_table.MethodB);
disp(pair_table);
end
