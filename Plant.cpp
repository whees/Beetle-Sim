// Plant.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#define N 64


using namespace std;


const int none = 0;
const int stem = 1;
const int flower = 2;
const int beetle = 3;


int cells[N][N];
int timers[N][N];
int ftimers[N][N];
bool pollens[N][N];
int xy[2] = {0,0};
const int tmax = 5;
const int ftmax = 200;
const int plant_scale = 10;





void update(int cells[N][N], int timers[N][N], int ftimers[N][N], bool pollens[N][N], int xy[2])
{

	for (int n = 0; n < 10; n++)
	{
		int x = xy[0];
		int y = xy[1];
		int i, j;
		int r = rand() % 100;
		if (r < 1)
		{
			i = 0.00 * x + 0.00 * y;
			j = 0.00 * x + 0.16 * y + 0.00;
		}
		else if (r < 85)
		{
			i = 0.91 * x + 0.00 * y;
			j = -0.0 * x + 0.86 * y + 1.60;
		}
		else if (r < 93)
		{
			i = 0.20 * x - 0.26 * y;
			j = 0.1 * x + 0.1 * y + 1.60;
		}
		else
		{
			i = -0.20 * x + 0.26 * y;
			j = 0.1 * x + 0.1 * y + 1;
		}
		



	

		int X = int((plant_scale * x + int(N / 2)));
		int Y = N - int(plant_scale * y);



		if (X > -1 && X < N && Y > -1 && Y < N && cells[X][Y] != flower)
		{
				cells[X][Y] = stem;
		}
		xy[0] = i;
		xy[1] = j;
	}



	for (int x = 0; x < N; x++)
	{
		for (int y = 0; y < N; y++)
		{
			int counts[4] = { 0,0,0,0 };

			for (int i = x - 1; i < x + 2; i++)
			{
				for (int j = y - 1; j < y + 2; j++)
				{
					if (i > -1 && i < N && j > -1 && j < N && (y != j || x != i))
					{
						int me = cells[i][j];
						if (me > -1 && me < 4)
						{
							counts[me] += 1;
						}
					}
				}
			}
			int me = cells[x][y];

			switch (me)
			{
			case beetle:
			{
				timers[x][y] -= 1;

				if (counts[beetle] > 3 || timers[x][y] < 1)
				{
					cells[x][y] = none;
					timers[x][y] = tmax;
				}

				else if (counts[stem] > 0 || counts[flower] > 0)
				{
					timers[x][y] = tmax;
				}

				if (counts[flower] > 0)
				{ 
					pollens[x][y] = true;
				}
				
					
			}
			case flower:
			{
				ftimers[x][y] -= 1;
				if (ftimers[x][y] < 1)
				{
					cells[x][y] = none;
					ftimers[x][y] = ftmax;
				}
			}
			case stem:
			{
				if (counts[beetle] > 0)
				{
					if (!pollens[x][y])
					{
						cells[x][y] = none;
					}
						
						
					else
					{
						int di = rand() % 100;
						if (di < 1 && counts[flower] > 0)
						{
							cells[x][y] = flower;
							pollens[x][y] = false;
						}
						else
						{
							cells[x][y] = none;
						}
					}

				}

			}
			default:
			{
				int di = rand() % 1000;
				
				if (di < 1 && !pollens[x][y] && counts[stem] == 3)
				{
					cells[x][y] = flower;

				}

				else if (di < 10 and pollens[x][y])
				{
					cells[x][y] = flower;
					pollens[x][y] = false;
				}

				else if (counts[beetle] > 0 and counts[stem] > 2)
				{
					cells[x][y] = beetle;
				}
					
			}
			}

		}
	}

	return;
}




int main()
{

	// initialize cells and timers
	for (int i = 0; i < N; i++)
	{
		for (int j = 0; j < N; j++)
		{
			cells[i][j] = 0;
			timers[i][j] = tmax;
			ftimers[i][i] = ftmax;
			pollens[i][j] = false;
		}
	}

	// main loop
	while (true)
	{
		// update cells
		update(cells, timers, ftimers, pollens,xy);

	}




	return 0;
}