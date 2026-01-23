import { motion } from 'framer-motion';
import { Download, CheckCircle, Network, ArrowLeft, Copy } from 'lucide-react';
import mermaid from 'mermaid';
import { useEffect, useRef, useState } from 'react';

mermaid.initialize({
  startOnLoad: true,
  theme: 'dark',
  securityLevel: 'loose',
  fontFamily: 'Inter',
});

function MermaidDiagram({ chart }) {
  const [svg, setSvg] = useState('');
  const [error, setError] = useState(null);

  useEffect(() => {
    const renderDiagram = async () => {
      if (!chart) return;
      try {
        setError(null);
        // Generate a unique ID for each render to prevent caching/selector collisions
        const id = `mermaid-${Math.random().toString(36).substr(2, 9)}`;
        const { svg } = await mermaid.render(id, chart);
        setSvg(svg);
      } catch (err) {
        console.error("Mermaid Render Error:", err);
        setError("Failed to render diagram. Syntax error likely.");
      }
    };

    renderDiagram();
  }, [chart]);

  if (error) return <div className="text-red-400 text-sm">{error}</div>;
  
  return (
    <div 
      className="flex justify-center w-full"
      dangerouslySetInnerHTML={{ __html: svg }}
    />
  );
}

export default function ResultsScreen({ result, onBack }) {
  const { code, explanation, diagram } = result;

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="w-full max-w-6xl mx-auto p-6 space-y-8"
    >
      <button 
        onClick={onBack}
        className="flex items-center text-muted-foreground hover:text-white transition-colors gap-2"
      >
        <ArrowLeft className="w-4 h-4" />
        Back to Input
      </button>

      {/* Grid Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* Architecture Diagram */}
        <div className="col-span-1 lg:col-span-2 bg-card border border-white/10 rounded-2xl p-8 shadow-xl">
          <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
            <Network className="w-5 h-5 text-primary" />
            Architecture Diagram
          </h2>
          
          <div className="flex items-center justify-center p-8 bg-black/20 rounded-xl border border-white/5 relative overflow-hidden group min-h-[300px]">
            <div className="absolute inset-0 bg-grid-white/[0.02] bg-[length:20px_20px]" />
             {/* Dynamic Mermaid Diagram */}
            <div className="relative z-10 w-full overflow-x-auto">
                 {diagram ? (
                    <MermaidDiagram chart={diagram} />
                 ) : (
                    <p className="text-muted-foreground text-center">No diagram generated.</p>
                 )}
            </div>
          </div>
        </div>

        {/* Explanation */}
        <div className="bg-card border border-white/10 rounded-2xl p-8 shadow-lg">
          <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
            <CheckCircle className="w-5 h-5 text-green-400" />
            Explanation
          </h2>
          <div className="prose prose-invert max-w-none text-muted-foreground">
            <p className="leading-relaxed whitespace-pre-line">{explanation}</p>
          </div>
        </div>

        {/* Terraform Code */}
        <div className="bg-card border border-white/10 rounded-2xl p-8 shadow-lg flex flex-col h-[500px]">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold flex items-center gap-2">
              <span className="font-mono text-blue-400">&lt;/&gt;</span>
              Terraform Code
            </h2>
            <div className="flex gap-2">
                <button 
                    onClick={() => navigator.clipboard.writeText(code)}
                    className="p-2 hover:bg-white/10 rounded-md transition-colors" 
                    title="Copy Code"
                >
                    <Copy className="w-4 h-4 text-white/70" />
                </button>
                <button className="flex items-center gap-2 px-3 py-1.5 bg-primary/20 text-primary hover:bg-primary/30 rounded-md text-sm font-medium transition-colors">
                <Download className="w-4 h-4" />
                Download
                </button>
            </div>
          </div>
          
          <div className="flex-1 overflow-auto bg-[#0d1117] rounded-xl p-4 font-mono text-sm border border-white/5 resize-none">
            <pre className="text-gray-300">
              <code>{code}</code>
            </pre>
          </div>
        </div>

      </div>
    </motion.div>
  );
}

