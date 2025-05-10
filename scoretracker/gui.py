from flask import Flask, render_template, request

app = Flask(__name__)

class CricketCalculator:
    def __init__(self):
        self.results = {}

    def bowler_calculator(self, overs, runs_conceded, wickets):
        overs = float(overs)
        runs_conceded = int(runs_conceded)
        wickets = int(wickets)
        economy = runs_conceded / overs if overs > 0 else 0
        return {
            "Overs": overs,
            "Runs Conceded": runs_conceded,  # Clarified label
            "Wickets": wickets,
            "Economy": round(economy, 2)
        }

    def fielder_calculator(self, fielder_num, catches, run_outs):
        catches = int(catches)
        run_outs = int(run_outs)
        total_contributions = catches + run_outs
        return {
            "Fielder": fielder_num,
            "Catches": catches,
            "Run-outs": run_outs,
            "Total Contributions": total_contributions
        }

    def batsman_calculator(self, runs, wickets):
        runs = int(runs)
        wickets = int(wickets)
        adjusted_score = runs - (5 * wickets)  # Your specified formula
        return {
            "Runs": runs,
            "Wickets": wickets,
            "Adjusted Score": max(adjusted_score, 0)
        }

@app.route('/', methods=['GET', 'POST'])
def calculator():
    calc = CricketCalculator()
    results = {}
    
    if request.method == 'POST':
        try:
            # Bowler calculation
            results['bowler'] = calc.bowler_calculator(
                request.form['bowler_overs'],
                request.form['bowler_runs_conceded'],  # Updated name
                request.form['bowler_wickets']
            )

            # Fielders calculation (10 fielders)
            fielders = {}
            for i in range(1, 11):
                fielders[f'fielder_{i}'] = calc.fielder_calculator(
                    i,
                    request.form[f'fielder_{i}_catches'],
                    request.form[f'fielder_{i}_runouts']
                )
            results['fielders'] = fielders

            # Batsmen calculation (2 batsmen)
            results['batsman1'] = calc.batsman_calculator(
                request.form['batsman1_runs'],
                request.form['batsman1_wickets']
            )
            results['batsman2'] = calc.batsman_calculator(
                request.form['batsman2_runs'],
                request.form['batsman2_wickets']
            )

        except ValueError:
            return render_template('calculator.html', error="Please enter valid numerical values", results=None)
        except Exception as e:
            return render_template('calculator.html', error=f"An error occurred: {e}", results=None)

    return render_template('calculator.html', results=results, error=None)

if __name__ == '__main__':
    app.run(debug=True)