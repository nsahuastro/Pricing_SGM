import numpy as np

def fair_odds(prob):
    if prob>0: 
        return 1/prob
    else: 
        return print( "Probability must be greater than 0" )

#-----
'''
For practice, we can simulate distributions (Normal for team points, Poisson for goals).
'''
#-----

# assuminh normal distribution for team points
teamA_mean=65
teamA_std=12
teamB_mean=60
teamB_std=12

# Poisson distribution for favorite players goal
fav_playerA_lambda=1.5 # average goals per match

# define correlation between team points and favorite player goals
rho_corr=0.4

#-----
'''
simulate random variatbles
team A is correlated with fav_player by rho_corr, we need a bivariate normal/gaussian distribution to set/preserve a correlation between them and later transform them to desired distributions
'''
#----

num_simulations=10000
corr_mean=[0,0]
cov_matrix=[[1,rho_corr],[rho_corr,1]]

#create correlated bivariate standard normal distribution for Team A points and Fav Player goals
corr_dist=np.random.multivariate_normal(corr_mean,cov_matrix,num_simulations)
print(corr_dist.shape)

#team points distribution
teamA_points_dist=teamA_mean + teamA_std*corr_dist[:,0]
print(len(teamA_points_dist))
teamB_points_dist=np.random.normal(teamB_mean,teamB_std,num_simulations)
print(len(teamB_points_dist))

#favorite player goals distribution (has to be dynamic and correlated with team A points)
player_volatality=0.5  #0 is none and 1 is high
fav_playerA_lambda_sim=fav_playerA_lambda*np.exp(player_volatality*corr_dist[:,1])

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
house_edge=0.05 #5% house edge
adjusted_odds_joint=fair_odds_joint*(1-house_edge)
#fair_odds=fair_odds(prob_joint_event)

print(f"Probability Team A wins: {prob_teamA_wins:.4f}")
print(f"Probability Fav Player A scores >=2 goals: {prob_fav_playerA_scores_g2:.4f}")
print(f"Probability Joint Event (Team A wins and Fav Player A scores >=2 goals): {prob_joint_event:.4f}")
print(f"Probability if Independent Events (Team A wins and Fav Player A scores >=2 goals): {prob_independent_events:.4f}")

print(f"Fair Oddss if Independent Events: {fair_odds(prob_independent_events)*(1-house_edge):.2f}")
print(f"Fair Odds for Joint Event (Team A wins and Fav Player A scores >=2 goals): {fair_odds_joint:.2f}")
print(f"Adjusted Odds for Joint Event (Team A wins and Fav Player A scores >=2 goals): {adjusted_odds_joint:.2f}")