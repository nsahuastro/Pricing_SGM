import numpy as np

def fair_odds(prob):
    if prob>0: 
        return 1/prob
    else: 
        return print( "Probability must be greater than 0" )

#-----
'''
A prototype sports betting simulation framework, to estimate prices for joint events
Simulating distributions (Normal for team points, Poisson for goals).
'''
#-----

# assuminh normal distribution for team points
teamA_mean=65
teamA_std=12
teamB_mean=60
teamB_std=12

# Poisson distribution for favorite player's distribution of goals across many matches
fav_playerA_lambda=1.5 # average goals per match

'''
defining correlation between team A points and Team A's favorite player's goals, and using this correlation to
simulate  Team A points and player goal's

I we had the actual historical data, the data distribution would intrinsically have this coorelation we could compute the correlation directly
'''

#assuming coorelation coefficient between team A points and favorite player goals
rho_corr=0.4


#-----
'''
simulate random variables - Team A Points, Team B Points, Fav Player A Goals- Monte Carlo (random/stochastic) Simulations
'''
#----

num_simulations=10000

'''
team A is supposed to be correlated with fav_player by rho_corr, so we build a biavariate gaussian distribution that has this correlation.
We then use this biavariate gaussian distribution to modulate the individual distributions of Team A points and Fav Player goals 
so that we have two random variables that are correlated according to rho_corr.
'''
#create correlated bivariate standard normal distribution (mean=0, std dev=1) for Team A points and Fav Player goals
corr_mean=[0,0]
cov_matrix=[[1,rho_corr],[rho_corr,1]]
corr_distribution=np.random.multivariate_normal(corr_mean,cov_matrix,num_simulations)
print(corr_distribution.shape)

#simulating team points distribution 
teamA_points_dist=teamA_mean + teamA_std*corr_distribution[:,0]
print(len(teamA_points_dist))
teamB_points_dist=np.random.normal(teamB_mean,teamB_std,num_simulations)
print(len(teamB_points_dist))

#favorite player goals distribution (has to be dynamic and correlated with team A points)
player_volatality=0.5  #0 is none and 1 is high
fav_playerA_lambda_sim=fav_playerA_lambda*np.exp(player_volatality*corr_distribution[:,1])

fav_playerA_goals_dist=np.random.poisson(fav_playerA_lambda_sim)
print(len(fav_playerA_goals_dist))

#---
'''
Define events or bet option
'''
#---

team_A_wins=teamA_points_dist>teamB_points_dist
fav_playerA_scores_g2=fav_playerA_goals_dist>=2
joint_event=team_A_wins & fav_playerA_scores_g2

#---
'''
estimate probabilities
'''
#---
prob_teamA_wins=np.mean(team_A_wins)
prob_fav_playerA_scores_g2=np.mean(fav_playerA_scores_g2)
prob_joint_event=np.mean(joint_event)
prob_independent_events=prob_teamA_wins*prob_fav_playerA_scores_g2


#---
'''
estimate Odds
'''
#---

fair_odds_joint=fair_odds(prob_joint_event)
house_edge=0.05 #5% house edge { this has to account for vig, operational costs, profit margin etc.}
adjusted_odds_joint=fair_odds_joint*(1-house_edge)
#fair_odds=fair_odds(prob_joint_event)

print(f"Probability Team A wins: {prob_teamA_wins:.4f}")
print(f"Probability Fav Player A scores >=2 goals: {prob_fav_playerA_scores_g2:.4f}")
print(f"Probability Joint Event (Team A wins and Fav Player A scores >=2 goals): {prob_joint_event:.4f}")
print(f"Probability if Independent Events (Team A wins and Fav Player A scores >=2 goals): {prob_independent_events:.4f}")

print(f"Fair Oddss if Independent Events: {fair_odds(prob_independent_events)*(1-house_edge):.2f}")
print(f"Fair Odds for Joint Event (Team A wins and Fav Player A scores >=2 goals): {fair_odds_joint:.2f}")
print(f"Adjusted Odds for Joint Event (Team A wins and Fav Player A scores >=2 goals): {adjusted_odds_joint:.2f}")