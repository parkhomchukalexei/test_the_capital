import asyncio
import aiohttp
from rest_framework.views import APIView, Response, status
from core.serializers import MatrixSerializer


class MatrixController(APIView):

    def get(self, request):

        url_matrix = [asyncio.run(get_matrix(SOURCE_URL))]

        test_matrix = [TRAVERSAL]

        one_more_test_matrix = [TRAVERSAL_2]
        data = [
            {'matrix_field': url_matrix},
            {'matrix_field': test_matrix},
            {'matrix_field': one_more_test_matrix},
        ]
        serializer = MatrixSerializer(data=data, many=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)


async def get_text(url: str) -> str | None:
    """Отримуемо текст матриці по url"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if 400 <= resp.status < 500:
                    print('There is Client Error')
                elif resp.status > 500:
                    print('Server error')
                else:
                    return await resp.text()
    except aiohttp.ClientError as e:
        print(f'Bad connection {e}')
    except asyncio.TimeoutError as e:
        print(f'Timeout error {e}')


def parse_matrix(text: str) -> list[list[int]]:
    """Виділяємо матрицю з тексту"""
    try:
        matrix = []
        for line in text.split('\n'):
            if line and line[0] != '+':
                matrix.append([int(num) for num in line[1:-1].split('|')])

        if matrix and not all([len(matrix) == len(line) for line in matrix]):
            raise ValueError("Matrix is not squared")
    except ValueError as ex:
        print(ex)
        return []

    return matrix


def traverse_matrix(matrix: list[list[int]] | list[tuple[int]],
                    output: list[int]) -> list[int]:
    """Обходимо матрицю по спіралі."""
    if output is None:
        output = []

    if not len(matrix):
        return output

    matrix = list(zip(*matrix[::-1]))
    output.extend(matrix[0][::-1])
    traverse_matrix(matrix[1:], output)




async def get_matrix(url: str) -> list[int]:
    """Отримуємо результат"""
    output = []
    text = await get_text(url)
    traverse_matrix(parse_matrix(text), output)
    return output


SOURCE_URL = 'https://raw.githubusercontent.com/Real-Estate-THE-Capital/python-assignment/main/matrix.txt'
TRAVERSAL = [
    10, 50, 90, 130,
    140, 150, 160, 120,
    80, 40, 30, 20,
    60, 100, 110, 70,
]

TRAVERSAL_2 = [
    55, 44, 25, 99, 130,
    66, 22, 44, 55, 11,
    87, 93, 12, 65, 90,
    11, 23, 45, 90, 76,
    11, 22, 33, 44, 55,
]




