import time
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback

from backend.blockchain.block import Block

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-96559dea-a91c-11ec-94c0-bed45dbe0fe1'
pnconfig.publish_key = 'pub-c-56836b25-04ac-4825-aead-671c8a91a944'

CHANNELS = {
    'TEST': 'TEST',
    'BLOCK': 'BLOCK'

}


class Listener(SubscribeCallback):
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def message(self, pubnub, message_object):
        print(f'\n-- Channel: {message_object.channel} | Message: {message_object.message}')

        if message_object.channel == CHANNELS['BLOCK']:
            block = Block.from_json(message_object.message)
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(block)

            try:
                self.blockchain.replace_chain(potential_chain)
                print('\n -- Succesyfuly replaced the local chain')
            except Exception as e:
                print(f'\n -- Did Not replace chain: {e}')
class PubSub():
    """
    Handles the publish/subscribe layer of the application.
    Provides comunication between the nodes of the blockchain network
    """
    def __init__(self, blockchain):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain))

    def publish(self, channel, message):
        self.pubnub.publish().channel(channel).message(message).sync()
    
    def broadcast_block(self, block):
        self.publish(CHANNELS['BLOCK'],block.to_json())

def main():
    pubsub = PubSub()

    time.sleep(1)

    pubsub.publish(CHANNELS['TEST'], {'foo': 'bar'})


if __name__ == '__main__':
    main()
