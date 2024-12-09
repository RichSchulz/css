# Effects of Altruistic Behavior on Schelling’s Segregation Model

This project explores how altruistic behavior and various relocation policies influence segregation dynamics in agent-based models. By extending the classical Schelling model, we introduce altruistic agents and diverse relocation mechanisms to evaluate their impact on collective utility and segregation outcomes.

---

## Dependencies

Ensure you have Python installed on your system. Install the required dependencies by running:

```bash
pip install -r requirements.txt
```

---

## Reproducing the Analysis

We provide several Jupyter notebooks for running simulations and analyzing the results. Note that some simulations can take several days to complete. To save you time, we have included precomputed results in the `__pycache__` directory, which can be directly utilized within the notebooks.

Available notebooks:

- **`analysis.ipynb`**: General analysis of simulation results.
- **`history_policy_analysis.ipynb`**: Investigates the effects of history-based relocation policies.
- **`analysis_different_altruism_levels.ipynb`**: Examines the impact of varying levels of altruism on segregation dynamics.

To run a notebook, use the command:

```bash
jupyter notebook <notebook_name>.ipynb
```

---

## References

This project builds on the following foundational works:

- Schelling, T. C. (1971). *Dynamic models of segregation*. *Journal of Mathematical Sociology*, 1(2), 143–186.
- Mauro, G., & Pappalardo, L. (2024). *Dynamics of Policy-Driven Segregation in Schelling Models*. In *Proceedings of the Workshops of the EDBT/ICDT 2024 Joint Conference* (March 25-28, 2024), Paestum, Italy. CEUR Workshop Proceedings.
- Jensen, P., Matreux, T., Cambe, J., Larralde, H., & Bertin, E. (2018). *Giant Catalytic Effect of Altruists in Schelling's Segregation Model*. *Physical Review Letters*, 120(20), 208301.

---

## Base Code

The base code for this project is adapted from [this repository](https://github.com/mauruscz/RS-chelling).
