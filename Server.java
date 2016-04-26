import java.io.*;
import java.net.*;

/**
 * Created by nick on 4/14/16.
 */
public class Server {
    
    private final static int BUFFER_SIZE = 1024;
    
    public static void main(String[] args) throws IOException{
        
        try {
            InetAddress addr = InetAddress.getLocalHost();
            System.out.println("Local host: " + addr.getHostAddress());
        } catch(UnknownHostException e) {
            System.out.println("how do you have an unknown local host?");
        }
        
        if(args.length < 1) {
            System.out.println("please give the port number");
            return;
        }
        
        int servPort = Integer.valueOf( args[0]); // assume the first argument is the port number
        
        System.out.println("Started server on port: " + servPort);
        
        ServerSocket serverSocket = new ServerSocket(servPort);

        File f = new File("./model");
        
        OutputStream fos = new FileOutputStream(f);
        fos.write("Sensor data:\n".getBytes());
        fos.close();
        
        int msgSize;
        byte[] byteBuffer = new byte[BUFFER_SIZE];
        
        for(;;) {
            Socket client = serverSocket.accept();
            System.out.println("got client: " + client.getInetAddress());
            
            InputStream is = client.getInputStream();
            OutputStream os = new FileOutputStream(f, true);
            
            while( (msgSize = is.read(byteBuffer))  > 0) {;
                //Write data to output file
                String data = new String(byteBuffer).trim();
                data = System.currentTimeMillis() + ": " + data + ";\n";
                os.write(data.getBytes());
                System.out.println(data.trim());
            }
            
            os.close();
            client.close();
        }
    }
}