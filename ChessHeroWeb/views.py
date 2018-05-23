from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import chess
import chess.uci
import chess.svg
import json

eg1 = chess.uci.popen_engine("./Engines/Hermann28_64.exe",
							 engine_cls=chess.uci.Engine)
eg2 = chess.uci.popen_engine("./Engines/stockfish_8_x64.exe",
							 engine_cls=chess.uci.Engine)
eg1.uci()
eg2.uci()

board = chess.Board()


# Create your views here.
@csrf_exempt
def showBoard(request):
	if request.method == 'POST':
		if request.POST.get('what') == 'start':
			if board.is_checkmate():
				return HttpResponse(json.dumps({
					'board': chess.svg.board(board, size=600),
					'checkmate': board.is_checkmate()
				}))
			else:
				if board.turn:
					eg1.position(board)
					result = eg1.go(movetime=3000)
				else:
					eg2.position(board)
					result = eg2.go(movetime=3000)
				board.push(result[0])
				return HttpResponse(json.dumps({
					'board': chess.svg.board(board, size=600),
					'checkmate': board.is_checkmate()
				}))
	else:
		context = {}
		context['eg1'] = eg1.name
		context['eg2'] = eg2.name
		context['board'] = chess.svg.board(board, size=600)
		return render(request, 'showboard.html', context)


@csrf_exempt
def start(request):
	print(233)
	pass
