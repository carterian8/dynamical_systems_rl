from django.shortcuts import render
import math

def index(request):
    return render(request, "tunesweeper/index.html", {})

def game_interface(request):
	
	num_rows_cols = int(request.POST["difficulty"])
	numbers = []
	
	for row in range(num_rows_cols):
		numbers.append([row] * num_rows_cols)
	
	## For materialize.css
	push_amount = int((12 - num_rows_cols) / 2)
	
	return render(
    	request,
    	"tunesweeper/game_interface.html",
    	{
    		"numbers" : numbers,
    		"push_amount" : push_amount
    	}
    )
