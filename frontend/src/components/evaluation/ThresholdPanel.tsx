type ThresholdPanelProps = {
  thresholds: Record<
    string,
    Record<string, number>
  >;
};


function formatMetric(
  value: string,
) {
  return value.replace(
    /_/g,
    " ",
  );
}


export function ThresholdPanel({
  thresholds,
}: ThresholdPanelProps) {
  return (
    <section className="evaluation-card">
      <div className="evaluation-card-heading">
        <div>
          <span className="eyebrow">
            Release Gates
          </span>

          <h3>
            Quality thresholds
          </h3>
        </div>
      </div>

      <div className="threshold-groups">
        {Object.entries(
          thresholds,
        ).map(
          ([
            evaluator,
            metrics,
          ]) => (
            <div
              key={evaluator}
              className="threshold-group"
            >
              <strong>
                {formatMetric(
                  evaluator,
                )}
              </strong>

              <div>
                {Object.entries(
                  metrics,
                ).map(
                  ([
                    metric,
                    value,
                  ]) => (
                    <span
                      key={metric}
                      className="threshold-pill"
                    >
                      {formatMetric(
                        metric,
                      )}

                      <b>
                        {value}
                      </b>
                    </span>
                  ),
                )}
              </div>
            </div>
          ),
        )}
      </div>
    </section>
  );
}