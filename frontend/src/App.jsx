import { useState } from 'react';
import InputScreen from './components/InputScreen';
import ResultsScreen from './components/ResultsScreen';
import { AnimatePresence, motion } from 'framer-motion';

// Mock Data for the PoC
const MOCK_TF_CODE = `provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "web" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.1.0/24"
}

resource "aws_instance" "app" {
  ami           = "ami-0c55b159cbfafe1f0" # Amazon Linux 2
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.web.id

  tags = {
    Name = "NodeApp-Ec2"
  }
}

resource "aws_lb" "app_lb" {
  name               = "app-load-balancer"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.lb_sg.id]
  subnets            = [aws_subnet.web.id]
}
# ... Mongo Atlas configuration would go here
`;

const MOCK_EXPLANATION = `Here is your generated infrastructure:

1. **AWS VPC**: A dedicated network environment for your resources.
2. **Load Balancer (ALB)**: Distributes incoming traffic across your Node.js instances to ensure high availability.
3. **EC2 Instance**: Hosts your Node.js application logic.
4. **MongoDB**: Your managed database instance for storing application data.

Traffic flows from the Load Balancer -> EC2 Nodes -> MongoDB.`;

function App() {
  const [screen, setScreen] = useState('input'); // 'input' | 'results'
  const [resultData, setResultData] = useState(null);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleGenerate = async (inputText) => {
    setError('');
    const text = inputText.toLowerCase();

    // 1. Validation Logic
    // Must NOT contain unsupported keywords
    const unsupported = ['kubernetes', 'k8s', 'docker', 'azure', 'gcp', 'lambda', 'serverless'];
    const foundUnsupported = unsupported.find(w => text.includes(w));
    if (foundUnsupported) {
       setError(`This infrastructure is not supported in the current PoC. We do not support ${foundUnsupported} yet.`);
       return;
    }

    // Must contain supported stack keywords (loose check for PoC friendliness)
    // "Only AWS Node.js EC2 + Load Balancer + MongoDB is supported"
    // RELAXED: strict check removed to allow AI to infer context (e.g. "three tier app" -> implies DB/LB)
    // We only check for explicitly WRONG things now (above).
    
    /* 
       Previously we enforced ['aws', 'node', 'mongo'] presence. 
       This was too strict for natural language (e.g. "three tier node app").
       We now let the backend decide if the intent matches the capabilities.
    */

    // 2. Real API Call
    setIsLoading(true);
    try {
        const response = await fetch('http://localhost:8000/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ description: inputText }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to generate infrastructure');
        }

        const data = await response.json();
        
        // Map backend response to frontend expected format
        setResultData({
            code: data.terraform_code,
            explanation: data.explanation,
            diagram: data.diagram
        });
        setScreen('results');
    } catch (err) {
        console.error("API Error:", err);
        setError(err.message || "An unexpected error occurred while connecting to the server.");
    } finally {
        setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen w-full bg-background text-foreground font-sans selection:bg-primary/20">
        {/* Simple Header */}
        <header className="fixed top-0 w-full p-6 z-50 flex justify-between items-center bg-background/50 backdrop-blur-md border-b border-white/5">
             <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-blue-500" />
                <span className="font-bold text-lg tracking-tight">AutoInfra.ai</span>
                <span className="text-xs px-2 py-0.5 rounded-full bg-white/10 ml-2">PoC</span>
             </div>
             <a href="#" className="text-sm font-medium hover:text-primary transition-colors">Documentation</a>
        </header>

         {/* Content Area */}
         <main className="pt-24 min-h-screen flex items-center justify-center relative overflow-hidden">
             {/* Ambient Background Glow */}
             <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-blue-500/10 rounded-full blur-[100px] -z-10" />
             
             <AnimatePresence mode="wait">
                {isLoading ? (
                    <motion.div
                        key="loading"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="flex flex-col items-center gap-4"
                    >
                        <div className="w-12 h-12 border-4 border-primary/30 border-t-primary rounded-full animate-spin" />
                        <p className="text-lg text-muted-foreground animate-pulse">Generating your infrastructure...</p>
                    </motion.div>
                ) : screen === 'input' ? (
                    <motion.div 
                        key="input"
                        exit={{ opacity: 0, scale: 0.95 }}
                        transition={{ duration: 0.3 }}
                        className="w-full"
                    >
                        <InputScreen onGenerate={handleGenerate} />
                        {error && (
                            <motion.div 
                                initial={{ opacity: 0, y: 10 }} 
                                animate={{ opacity: 1, y: 0 }}
                                className="mx-auto max-w-md mt-6 p-4 bg-red-500/10 border border-red-500/20 text-red-200 rounded-lg text-center text-sm"
                            >
                                {error}
                            </motion.div>
                        )}
                    </motion.div>
                ) : (
                    <motion.div
                        key="results"
                        exit={{ opacity: 0, scale: 1.05 }}
                        transition={{ duration: 0.3 }}
                        className="w-full"
                    >
                        <ResultsScreen 
                            result={resultData} 
                            onBack={() => setScreen('input')} 
                        />
                    </motion.div>
                )}
             </AnimatePresence>
         </main>

         {/* Footer */}
         <footer className="fixed bottom-0 w-full p-4 text-center text-xs text-muted-foreground/40 bg-background/80 backdrop-blur-sm border-t border-white/5">
            AutoInfra.ai uses AI to understand infrastructure requirements and generates safe, pre-defined cloud configurations using Terraform.
         </footer>
    </div>
  );
}

export default App;
