# Report

Simulating the evolution of a blockchain
 - Blockchain: append-only data structure
 - decentralized peer-to-peer distributed consensus protocol
 - probabilistic security guarantee


Notable differences from bitcoin:

 - Bitcoin's hashcash function uses SHA-256 twice to protect from possible birthday attacks, a known vulnerabilitiy in SHA-1. For our simple implementation, we only hash once to reduce the amount of computations.
 - No transaction scripting. We only implement the simplest and by far the most widely used transaction script. 


Merkle Tree:
 - summarizes the data, allowing for significant bandwith savings
 - disconnects the validation from the data itself by using hash and reduction functions


Identities:
Any user of the system can creaty any number of nodes. No real identity verification is required.


Block contains:
 - nonce
 - a hash of the previous block in the blockchain
 - a set of transactions
 - address of the block node that created the block


    version: 1,
    hash: 00000000000001f5af1,
    difficulty,
    nonce: 87434154,
    merkle_root: "hash of the root",
    num_tx: 354,
    size: "in bytes",
    tx: [], // array of transactions, coinbase tx first
    merkle_tree: [
        "hashes", // hashes of the merkle tree nodes, including coinbase transaction
    ]

Transacton contains:
 - transaction id (hash?)
 - hash to previous transaction where that coin came from
 - input amount
 - input address of the source participant node
 - output amount
 - output address of the destination participant node
 - amount (points)

   metadata: {
    version: 1,
    num_inputs,
    num_outputs,
    size: bytes,
    tx_hash: csdcsdcvc,
    lock_time: 0  # not valid before
   },
   inputs: [
    {
        out_prev: { tx_hash, idx },
        signature (with the public key K)
    }
   ],
   outputs: [
    { 
        value, 
        script: public key K
    }
   ]


    // coinbase transaction:
   metadata: {
    as usual,
   },
   coinbase: "", // arbitrary data
   coinbase_nonce,
   inputs: [
    {
        out_prev: { 
            tx_hash: "0",  // no input
            idx: -1,
        },
        signature (with the public key K)
    }
   ],
   outputs: [
    { 
        value: 12.5337..., // block reward + sum of transaction fees
        script: public key K 
    }
   ]


Mining:
for coinbase_nonce in 0..int_max:
    compute_merkle_tree()
    for block_nonce in 0..int_max:
        hash = hash(block)
        if hash < target:
            return block_nonce, coinbase_nonce, hash
return none



Transaction rules:
 - Outputs completely consume the inputs. If outputs are greater than inputs, the transaction is invalid. Any excess is considered as a transaction fee and is being collected by the block creator node into its coinbase transaction.

    if(total_input < total_output):
        return "invalid"

    tx_fee_amount = total_input - total_output

 - Backwards search in blockchain is performed to validate that the requesting node ras right to spend the specified inputs. Validation is performed by comparing signatures of every input with the public key of the requesting node.



Transaction 1: "Alice creates 25 BTC by discovering a new block"
Inputs: none
Outputs: 
    0: (25, Alice)
Signature: none

Transaction 2: "Alice pays 17 BTC to Bob"
Inputs: 1::0 (transaction 1, output 0)
Outputs: 
    0: (17, Bob)
    1: (8, Alice) // "Change". Sends excess back to the original owner
Signature: Alice

Transaction 3: "Bob pays 8 BTC to Charlie"
Inputs: 2::0
Outputs: 
    0: (8, Charlie)
    1: (7, Bob)
Signature: Bob

Transaction 4: "Alice pays 6 BTC to David"
Inputs: 2::1
Outputs: 
    0: (6, David)
    1: (2, Alice)
Signature: Alice

Transaction 5: "Bob merges his amounts"
Inputs: 2::0, 3::1
Outputs: 
    0: (24, Bob)
Signature: Bob

Transaction 6: "Alice and David jointly pay to Frank"
Inputs: 4.0, 4.1
Outputs: 
    0: (8, Frank)
Signature: Alice, David


Default transaction fee and tx acceptance:
tx accepted if priority > 0.576
priority = sim(intup_valie * input_age) / bytesize




Participant (end-user) node :
 - register with block nodes (one or several)
 - send transaction requests from block nodes
 - accept reward by block nodes (subscribed to)
 - exchange points with other participant nodes
 - perform tasks to gain merit from block nodes

Block (mining) node: has all attributes of participant nodes, but also competes for block proposal.

 - manage, update blockchain
 - accept or deny the registration transactions from participant nodes
 - accept transactions from participant nodes
 - create blocks
    - proof of work: in order to gain a right to produce a block, node is required to solve the computational puzzle (Bernoulli trial):
        - what string to add to the block so that hash starts with N zeros
        (greater N meas greater difficulty, may increase with time)
    - target difficulty recalculation every 2 weeks, so that average block latency (time between blocks) stays about 10 min

 - add pending transactions into blocks
 - to/from neighbouring block nodes:
    - retransmit transactions received from participant nodes
    - transmit newly created blocks
    - request the entire blockchain or its part
 - update blockchain
 - reward subscribed block nodes
 - can change the merit of registered participant nodes (fraction of generated blocks received)



Distributed consensus protocol:
Honest nodes extend the longest valid branch.

 - accept valid branches only
 - if different length, the longest branch is valid
 - if same length, the chain that came first is valid


Visualization:
 - number of blocks
 - contents of each block

Robustness:
 - Check that malicious node cannot corrupt the blockchain
 - Encrypt transactions with key pairs
 - 

Security and possible atack scenarios:

 - Stealth: with a malicious intent, Alice tries fakes Bob's transactions. As transactions are signed cryptographically, nodes will reject these transactions. The attack is impossible as long as cryptographic protection is functional.
 

 - Punitive forking, denial of service: with a malicious intent, Alice never includes Bob's transactions into blockchain when it's her turn to propose the next block. Another node will include it eventually. As long as Alice don't control the most of the work power of nodes (and block creation), the attack cannot succeed.

 - Deep forks, double spending attack and probabilistic guarantee: having a malicious intent Ailce broadcasts a transaction pointing to some previous transaction (for xample paying for a purchase and receiving the item). Later, some honest node proposes this transaction into the next block in the blockchain. If it so happens that the next chosen node is Alice's node, t will propose an alternative block, with another transaction (for example, with coin transfer to another node controlled by her), pointing to the same previous transaction (effectively canceling the payment). If it so happens that the next chosen node will be a malicious node, it will extend the alternative, malicious branch again. However probability of picking it correlates with the fraction of total work power of all nodes Alice controls. Double-spending probability drops exponentially with number of blockchain extensions, as long as more than half of compute (and block extensions) is contolled by honest nodes.
 The attack is easily detactable and the community may reverse the attack by rejecting the malicious branch. However, if succeeded, such attack may ruin peoples' trust in network and crash the exchange rate of the currency.

 - Block-withholding attack
Alice and Bob both have mining nodes and discover new blocks. Bob honestly publies his blocks. However, Alice holds discovered blocks and does not propose them to the network, effectively creating a hidden branch. After some time, Alics publishes her hidden blocks all at once. If Alice's branch is longer than current longest branch, then Alice's branch becomes the valid branch and all Bob's calculations and profit are invalidated. This is a variant of attack that does not lead to additional profit but instead hurts potential competitors. Block-withholding attack is possible to implement only possessing significant fraction of recources of the network, however, majority is not necessary.



Proof of work (proof-of-stake): 
In order to approximate the selection of the random mode in a distributed environment.
Select a node with a probability proportinal to a fracion of total amount of non-monopolizable resource that a node possesses.
Hash puzzle: find a string (nonce) that, when being appended to a block, produces a hash that maps to only a small part (target space) of the whole hashing space. The only way to find a nonce is to try large amount of different nonces, until finding a nonce that verifies:

H(nonce + prev_hash + tx + ... + tx)  < target

In bitcoin, the fraction of hashing space, and, thus, the difficluty, is being re-adjusted every 2 weeks to maintain the average block creation time of about 10 min.




Incentives: nodes are encouraged to behave honestly  and follow the protocol.
 Block reward: node that creates a block can include a special coin-creation transaction with address recepient of self. For bitcoin it is fixed and halves every ~4 years (currently 12.5 BTC).
Transaction fee: creator of transaction can voluntarily choose to include a bonus for a node that includes this fee into the extended block.

The bitcoin is secure if majority of nodes weighted by work power are honest (follow the protocol).


No ground truth:

As the system is peer-to-peer and there are no explicit synchronizations mechanisms, there is no unified blockchain state possible. Every node posesses it's own view into the blockchain and distributed consensus protocol dictates which parts of any of these views of are valid. Even the amount of coins a node owns is a subject to consensus. The absence of a ground truth version of blockchain has direct consequences for the visualization of the system.


ASIC-resistant puzzles

Memory-hard puzzle: scrypt

In scrypt this puzzle, SHA-256 is replaced with scrypt function. Scrypt is a memory read/write intensive algorithm. As speed of memory hardware (such as random-access memory, NAND memory or hard disks) grows at much slower rates than speed of computational units (such as CPUs, GPUs, FPGAs and ASICs). Replacing computationally-intensive SHA-256 to a memory-intensive algorithm would reduce the concentation of power in the hands of major silicon hardware manufacturerers and retailers.

Useful puzzles:
SHA-256 computation has no purpose outside of the system and the power and environmental impact are wasted.
Primecoin: find Cunningham chain
Permacoin: stoage-based puzzle. Re-utilization of old hardware, rather than wasting manufacturing resources on producing ASICs that are quickly obsoleted and are thrown away.

Virtual mining (Proof-of-stake):
??

 ? Hard/soft forks

