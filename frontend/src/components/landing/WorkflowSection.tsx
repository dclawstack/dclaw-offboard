"use client";

import content from "@/data/landing-content.json";

export default function WorkflowSection() {
  const { workflow } = content;

  return (
    <section className="py-20 sm:py-28 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold text-gray-900">
            {workflow.title}
          </h2>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
          {workflow.steps.map((step) => (
            <div key={step.number} className="relative text-center">
              <div className="w-14 h-14 rounded-2xl bg-white border-2 border-gray-200 flex items-center justify-center mx-auto mb-4">
                <span className="text-xl font-bold text-gray-900">{step.number}</span>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">{step.title}</h3>
              <p className="text-sm text-gray-500 leading-relaxed">{step.description}</p>

              {step.number < 4 && (
                <div className="hidden lg:block absolute top-7 left-[calc(50%+2rem)] w-[calc(100%-4rem)] h-0.5 bg-gradient-to-r from-gray-200 to-transparent" />
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
