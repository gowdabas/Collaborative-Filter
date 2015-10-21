import sys
import math

main_dict={}
inner_dict={}

def find_co_rated_movies(user1,user2,co_rated_movies_list):
	for key,value in main_dict[user1].items():
		if key in main_dict[user2]:
			co_rated_movies_list.append(key)
	return co_rated_movies_list

def find_avg(user,co_rated_movies_list,x):
	if x==0:
		user_avg=0
		for each in co_rated_movies_list:
			user_avg=user_avg+float(main_dict[user][each])
		user_avg=user_avg/len(co_rated_movies_list)
		return user_avg
	elif x==1:
		user_avg=0
		for key,value in main_dict[user].items():
			user_avg=user_avg+float(value)
		user_avg=user_avg/len(main_dict[user])
		return user_avg

def pearson_corelation(user1,user2):
	numerator=0
	denominator=0
	sum_user1=0
	sum_user2=0
	co_rated_movies_list=[]
	co_rated_movies_list=find_co_rated_movies(user1,user2,co_rated_movies_list)
	user1_total_avg=find_avg(user1,co_rated_movies_list,1)
	user2_total_avg=find_avg(user2,co_rated_movies_list,1)
	for each in co_rated_movies_list:
		numerator=numerator+(float(main_dict[user1][each])-user1_total_avg)*(float(main_dict[user2][each])-user2_total_avg)
	for each in co_rated_movies_list:
		sum_user1=sum_user1+math.pow((float(main_dict[user1][each])-user1_total_avg),2)
		sum_user2=sum_user2+math.pow((float(main_dict[user2][each])-user2_total_avg),2)
	denominator=math.sqrt(sum_user1)*math.sqrt(sum_user2)
	pearson_corelation_value=numerator/denominator
	return pearson_corelation_value	


def k_nearest_neighbours(user,k):
	k_neighbours_list=[]
	for key,value in main_dict.items():
		if key!=user:
			temp_list=[]
			temp_list.append(key)
			temp_list.append(pearson_corelation(user,key))
			k_neighbours_list.append(temp_list)
	return sorted(k_neighbours_list,key=lambda x:(x[1],x[0]),reverse=True)[:int(k)]
	
def Predict(user,item,k_nearest_neighbours_list):
	numerator=0
	denominator=0
	co_movie_list=[]
	final_k_neighbours_list=[]
	for each in k_nearest_neighbours_list:
		if item in main_dict[each[0]]:
			final_k_neighbours_list.append(each)
	user1_avg=find_avg(user,find_co_rated_movies(user,user,co_movie_list),0)
	for each in final_k_neighbours_list:
		co_movie_list=[]
		for i in main_dict[each[0]]:
			if i!=item:
				co_movie_list.append(i)
		numerator=numerator+((float(main_dict[each[0]][item]))*each[1])
		denominator=denominator+each[1]
	return (numerator/denominator)
	

def main(input_data,user_id,movie_name,k):
	k_nearest_neighbours_list=[]
	for line in input_data:
		input_list=line.strip().split('\t')
		if input_list[0] not in main_dict:
			main_dict[input_list[0]]={}
			main_dict[input_list[0]][input_list[2]]={}
			main_dict[input_list[0]][input_list[2]]=input_list[1]
		else:	
			main_dict[input_list[0]][input_list[2]]=input_list[1]
	k_nearest_neighbours_list=k_nearest_neighbours(user_id,k)	
	predicted_rating=Predict(user_id,movie_name,k_nearest_neighbours_list)

	for i in range(0,len(k_nearest_neighbours_list)):
		print k_nearest_neighbours_list[i][0], k_nearest_neighbours_list[i][1]	
	print '\n'		
	print predicted_rating	
 	
			
 
input_data=open(sys.argv[1],'r')
user_id=sys.argv[2]
movie_name=sys.argv[3]
k=sys.argv[4]
main(input_data,user_id,movie_name,k)