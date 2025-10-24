# gogostats
Go Go Muffin game statistics services

## Hosting your own server
1. Copy .example.env to .env and modify variables for your needs
2. Run docker compose:
   ```
   docker compose up -d --build
   ```

## Autocollecting
You can write pm me in telegram [@HelgLeshiy](http://t.me/HelgLeshiy) and pass your User ID (look at user center) and Character ID. And I will run autocollection for your character guild and server dragon dmg

## Using proxy for collecting data
1. Install any socks5 proxy client on your device with game (for example Tun2Socks for Android)
2. Enter gogo mitm proxy address and port (main server is stream1.transcriptic.ru 5800). Dont connect.
3. Open game, authorize and enter server
4. Turn on proxy connection
5. Now you can collect data by opening guild member list and scrolling and clicking any player info you can find.
6. Don't forget to turn off proxy connection, because you haven't installes certificates and you will not receive any TLS data while being connected

## Researching
You can help and continue research and reverse game traffic.
You need:
1. Android emulator with game on your PC (for example MuMuPlayer)
2. Install game normally
3. Run game and enter server
4. Install Wireshark for traffic sniffing and analysis
5. Start Wireshark session on your network interface
6. Do some necessary things in game and stop capturing
7. Search for some strings and data in captured packets
8. Inspect for differences between same actions in packets
9. Copy tcp packet data as hexademical flow and paste to https://protobuf-decoder.netlify.app/
10. Delete some leading bytes before you get clean protobuf (you can also play with leading length prefix, I got this useful in parsing PlayerInfo)
11. Contribute to this repository:
    - Modify gogoproxy/messages.proto in rules of protobuf version 3
    - Compile protobuf to python classes:
    ```shell
    python -m grpc_tools.protoc --proto_path . --pyi_out . --python_out=. messages.proto
    ```
    - Then you can modify tcpaddon for mitm proxy, that parses this protobuf messages. You can use leading bytes as flag to catch this specific type of protobuf message.
    - Modify backend/main.py to support your new prometheus metrics and may be new Flask endpoints to pass data
    
