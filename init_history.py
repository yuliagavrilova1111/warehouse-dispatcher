import asyncio
import sys
sys.path.append('.')
from src.database import save_history

async def main():
    sample_row = {
        'timestamp': '2025-05-30T10:00:00',
        'target_2h': 100.0,
        'status_1': 0,
        'status_2': 46,
        'status_3': 0,
        'status_4': 0,
        'status_5': 12,
        'status_6': 9,
        'status_7': 0,
        'status_8': 0
    }
    await save_history(0, sample_row)
    print('History added for route 0')

if __name__ == '__main__':
    asyncio.run(main())