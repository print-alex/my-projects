from re import L
from tkinter import E
from backend.blockchain.block import Block


class Blockchain:

    """
    Blockchain: a public ledger of transactions
    Implemented as a list of blocks - data sets of transactions
    """

    def __init__(self):
        self.chain = [Block.genesis()]

    def add_block(self, data):
         self.chain.append(Block.mine_block(self.chain[-1], data))

    def __repr__(self):
        return f'Blockchain:{self.chain}'

    def replace_chain(self, chain):
        """
        Replace the local chain with incoming one if the fallowing applies:
            - The incoming chain is longer than the local one
            - The incoming chain is formated properly
        """
        if len(chain) <= len(self.chain):
            raise Exception('Cannot replace.The incoming chain must be longer.')

        try:
            Blockchain.is_valid_chain(chain)
        except Exception as e:
            raise Exception(f'Cannot replace.The incoming chain is invalid : {e}')

        self.chain = chain 

    def to_json(self):
        """
        Serialize the blockchain into a list of blocks
        """        
        return list(map(lambda block: block.to_json(), self.chain))

    @staticmethod
    def from_json(chain_json):
        blockchain = Blockchain()
        blockchain.chain = list(
            map(lambda block_json: Block.from_json(block_json),chain_json)
        )
        return blockchain

    @staticmethod
    def is_valid_chain(chain):
        """
        Validate incoming chain
        Enforce the following rules:
            - the chain must start with genesis block
            - block must be formated correctly
        """
        if chain[0] != Block.genesis():
            raise Exception('The genesis block must be valid')
        
        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i-1]
            Block.is_valid_block(last_block, block)




def main():
    blockchain = Blockchain()
    blockchain.add_block('one')
    blockchain.add_block('two')
    print(blockchain)
    print(f'blockchain.py __name__: {__name__}')


if __name__ == '__main__':
    main()
